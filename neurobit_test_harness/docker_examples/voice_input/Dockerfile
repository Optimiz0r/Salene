FROM python:3.11-slim

WORKDIR /app

# Install dependencies for voice processing
RUN pip install --no-cache-dir \
    faster-whisper \
    numpy \
    uvicorn \
    starlette \
    mcp

# Copy the MCP server implementation
COPY mcp_server.py .

EXPOSE 8000

CMD ["python", "mcp_server.py"]
