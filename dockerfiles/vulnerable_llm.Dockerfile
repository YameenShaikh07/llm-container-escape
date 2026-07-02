FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install flask requests

# Simulate an LLM inference service with common misconfigurations
COPY app.py /app/app.py

# Intentionally vulnerable: running as root (common misconfig)
# Intentionally vulnerable: no read-only filesystem
# Intentionally vulnerable: exposed unnecessary capabilities

EXPOSE 5000

CMD ["python", "app.py"]
