# Voice Input MCP Server

Docker-based voice transcription "organ" for Neurobit Agent.

## Building
```bash
docker build -t neurobit-voice-input .
```

## Running
```bash
docker run -p 8000:8000 neurobit-voice-input
```

## MCP Config (in ~/.hermes/config.yaml)
```yaml
mcp_servers:
  voice_input:
    command: "docker"
    args: ["run", "-i", "neurobit-voice-input"]
```
