# Use lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# ensure alembic and postgres driver are available in the image
RUN pip install --no-cache-dir alembic psycopg2-binary

# Copy source code
COPY . .
# make start script executable
RUN chmod +x ./start.sh

# Expose FastAPI default port
EXPOSE 8000

# Start the FastAPI app
ENTRYPOINT ["/bin/sh", "./start.sh"]
