#!/usr/bin/env python3
"""
Voice Input MCP Server
Docker-based "organ" that provides voice-to-text for Neurobit Agent
"""

import asyncio
import numpy as np
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    TextContent,
    Tool,
)

# Initialize faster-whisper model (downloads on first run)
print("Loading faster-whisper model...", file=sys.stderr)
from faster_whisper import WhisperModel
model = WhisperModel("base", compute_type="int8")

app = Server("voice-input")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="transcribe_audio",
            description="Transcribe audio bytes to text using faster-whisper",
            inputSchema={
                "type": "object",
                "properties": {
                    "audio_bytes": {
                        "type": "string",
                        "description": "Base64-encoded audio data (WAV format preferred)"
                    },
                    "language": {
                        "type": "string", 
                        "description": "Optional language code (e.g., 'en')"
                    }
                },
                "required": ["audio_bytes"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "transcribe_audio":
        import base64
        import tempfile
        import os
        
        # Decode audio
        audio_bytes = base64.b64decode(arguments["audio_bytes"])
        
        # Write to temp file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            f.write(audio_bytes)
            temp_path = f.name
        
        try:
            # Transcribe
            segments, info = model.transcribe(
                temp_path, 
                language=arguments.get("language"),
                beam_size=5
            )
            
            text = " ".join([segment.text for segment in segments])
            
            return [TextContent(
                type="text",
                text=json.dumps({
                    "text": text,
                    "language": info.language,
                    "probability": info.language_probability
                })
            )]
        finally:
            os.unlink(temp_path)
    
    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    import sys
    import json
    asyncio.run(main())
