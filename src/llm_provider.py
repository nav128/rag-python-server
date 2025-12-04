import asyncio
from datetime import time
from config import LLM_PROVIDER
import httpx
import logging
import json
from typing import AsyncGenerator
from pydantic import BaseModel

from config import OPENAI_API_KEY

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChatMessage(BaseModel):
    role: str  # "user", "assistant", "system"
    content: str
    timestamp: str | None = time().isoformat()


async def stream_llm_response(
    messages: list[ChatMessage],
    model: str = "gpt-4",
    temperature: float = 0.7,
) -> AsyncGenerator[str, None]:
    """
    Stream LLM response from OpenAI API.

    Args:
        messages: List of ChatMessage objects.
        model: OpenAI model name (default: gpt-4).
        temperature: Sampling temperature.

    Yields:
        Token/chunk strings from OpenAI.
    """
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY not set in config")

    logger.info(f"Model: {model}, Messages: {len(messages)}, Provider: openai")

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [{"role": m.role, "content": m.content} for m in messages],
        "temperature": temperature,
        "stream": True,
    }

    try:
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream("POST", url, json=payload, headers=headers) as response:
                logger.info(f"OpenAI response status: {response.status_code}")
                
                if response.status_code != 200:
                    text = await response.aread()
                    logger.error(f"OpenAI error: {text.decode(errors='replace')}")
                    raise RuntimeError(f"OpenAI HTTP {response.status_code}")

                async for raw_line in response.aiter_lines():
                    if not raw_line:
                        continue
                    
                    line = raw_line.strip()
                    
                    # Handle SSE format: "data: {...}"
                    if line.startswith("data:"):
                        data_str = line[5:].strip()
                    else:
                        data_str = line
                    
                    # Skip stream markers
                    if data_str in ("[DONE]", ""):
                        break
                    
                    try:
                        data = json.loads(data_str)
                        # Extract content from choices[0].delta.content
                        if "choices" in data and len(data["choices"]) > 0:
                            delta = data["choices"][0].get("delta", {})
                            content = delta.get("content")
                            if content:
                                yield content
                    except json.JSONDecodeError:
                        logger.debug(f"Skipped invalid JSON: {data_str}")
                        continue
                        
    except Exception as e:
        logger.error(f"OpenAI streaming error: {str(e)}")
        raise

