from sqlalchemy.orm import Session

from . import models, schemas
import logging

logger = logging.getLogger("todo-app.crud")


def get_todos(db: Session, skip: int = 0, limit: int = 100):
    res = db.query(models.Todo).offset(skip).limit(limit).all()
    logger.info("DB READ get_todos skip=%s limit=%s count=%s", skip, limit, len(res))
    return res


def create_todo(db: Session, todo: schemas.TodoCreate):
    db_todo = models.Todo(content=todo.content, due=todo.due)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    logger.info("DB WRITE create_todo id=%s content=%s", db_todo.id, todo.content)
    return db_todo


def update_todo(db: Session, todo_id: int, done: bool):
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not db_todo:
        return None
    db_todo.done = done
    db.commit()
    db.refresh(db_todo)
    logger.info("DB UPDATE todo id=%s done=%s", todo_id, done)
    return db_todo


def get_todo(db: Session, todo_id: int):
    res = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    logger.info("DB READ get_todo id=%s found=%s", todo_id, bool(res))
    return res


def delete_todo(db: Session, todo_id: int):
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not db_todo:
        return None
    db.delete(db_todo)
    db.commit()
    logger.info("DB DELETE todo id=%s", todo_id)
    return db_todo
