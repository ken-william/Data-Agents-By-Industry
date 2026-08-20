FROM python:3.10-slim

WORKDIR /app

# Install python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir fastapi uvicorn sse-starlette pydantic requests

# Copy source code and prebuilt frontend
COPY . .

# Environment variables
ENV PORT=8080
ENV GOOGLE_CLOUD_PROJECT=data-agents-by-industry

EXPOSE 8080

CMD ["python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"]
