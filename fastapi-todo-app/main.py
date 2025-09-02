from fastapi import FastAPI, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import json
import logging

from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine
from redis_client import connect_redis, close_redis, get_redis

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# simple logger for cache/db diagnostics
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("todo-app")

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
async def on_startup():
    # connect to redis at startup (compose service name 'redis')
    await connect_redis("redis://redis:6379/0")
    r = get_redis()
    if r:
        logger.info("Redis client connected")
    else:
        logger.info("Redis client not available (skipping)")


@app.on_event("shutdown")
async def on_shutdown():
    await close_redis()
    logger.info("Shutdown: closed redis client (if any)")


@app.get("/todos")
async def read_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    r = get_redis()
    cache_key = f"todos:all:{skip}:{limit}"
    if r:
        cached = await r.get(cache_key)
        if cached:
            logger.info("CACHE HIT %s", cache_key)
            return json.loads(cached)
        else:
            logger.info("CACHE MISS %s", cache_key)

    todos = crud.get_todos(db, skip, limit)
    payload = jsonable_encoder(todos)

    if r:
        await r.set(cache_key, json.dumps(payload), ex=60)
    logger.info("CACHE SET %s (ttl=60s)", cache_key)
    return payload


@app.post("/todos")
async def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    db_todo = crud.create_todo(db, todo)
    logger.info("DB WRITE create todo id=%s content=%s", getattr(db_todo, "id", None), todo.content)
    r = get_redis()
    if r:
        # invalidate lists cache
        async for key in r.scan_iter("todos:all*"):
            logger.info("CACHE DELETE %s", key)
            await r.delete(key)
    return db_todo


@app.put("/todos/{todo_id}")
async def update_todo(todo_id: int, done: bool, db: Session = Depends(get_db)):
    db_todo = crud.update_todo(db, todo_id, done)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    logger.info("DB UPDATE todo id=%s done=%s", todo_id, done)
    r = get_redis()
    if r:
        await r.delete(f"todos:{todo_id}")
        logger.info("CACHE DELETE todos:%s", todo_id)
        async for key in r.scan_iter("todos:all*"):
            logger.info("CACHE DELETE %s", key)
            await r.delete(key)
    return db_todo



@app.get("/todos/{todo_id}")
async def read_todo(todo_id: int, db: Session = Depends(get_db)):
    r = get_redis()
    cache_key = f"todos:{todo_id}"
    if r:
        cached = await r.get(cache_key)
        if cached:
            logger.info("CACHE HIT %s", cache_key)
            return json.loads(cached)
        else:
            logger.info("CACHE MISS %s", cache_key)

    db_todo = crud.get_todo(db, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    payload = jsonable_encoder(db_todo)
    if r:
        await r.set(cache_key, json.dumps(payload), ex=60)
    logger.info("CACHE SET %s (ttl=60s)", cache_key)
    return payload


@app.delete("/todos/{todo_id}")
async def remove_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = crud.delete_todo(db, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    logger.info("DB DELETE todo id=%s", todo_id)
    r = get_redis()
    if r:
        await r.delete(f"todos:{todo_id}")
        logger.info("CACHE DELETE todos:%s", todo_id)
        async for key in r.scan_iter("todos:all*"):
            logger.info("CACHE DELETE %s", key)
            await r.delete(key)
    return {"ok": True, "deleted": todo_id}
