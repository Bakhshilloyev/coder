# Minimal, dependency-free API server image.
FROM python:3.11-slim

WORKDIR /app

# Copy only what's needed to run the agent.
COPY pyproject.toml requirements.txt ./
COPY src ./src
COPY configs ./configs
COPY prompts ./prompts

ENV PYTHONPATH=/app/src
ENV LOG_LEVEL=INFO
ENV MODEL_PROVIDER=local

EXPOSE 8000
CMD ["python", "-m", "agent.main", "server", "--host", "0.0.0.0", "--port", "8000"]
