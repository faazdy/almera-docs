"""Cliente mínimo de OpenRouter con streaming (API compatible con OpenAI)."""

import json
import ssl
from collections.abc import AsyncIterator

import httpx
import truststore

from . import config

# Usa los certificados de Windows/macOS en vez de los de certifi: la red corporativa
# inspecciona TLS con un certificado propio que solo está en el almacén del sistema.
SSL_CONTEXT = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)


class LLMError(Exception):
    pass


async def stream_chat(messages: list[dict]) -> AsyncIterator[str]:
    if not config.OPENROUTER_API_KEY:
        raise LLMError("Falta OPENROUTER_API_KEY en rag/.env")

    payload = {
        "model": config.OPENROUTER_MODEL,
        "messages": messages,
        "stream": True,
        "temperature": 0.2,
    }
    if config.OPENROUTER_DENY_DATA_COLLECTION:
        payload["provider"] = {"data_collection": "deny"}

    headers = {
        "Authorization": f"Bearer {config.OPENROUTER_API_KEY}",
        "X-Title": "SABIA - Almera RAG",
    }

    async with httpx.AsyncClient(timeout=httpx.Timeout(120, connect=10), verify=SSL_CONTEXT) as client:
        async with client.stream("POST", config.OPENROUTER_URL, json=payload, headers=headers) as resp:
            if resp.status_code != 200:
                body = (await resp.aread()).decode("utf-8", "replace")
                try:
                    detail = json.loads(body)["error"]["message"]
                except (ValueError, KeyError, TypeError):
                    detail = body[:300]
                raise LLMError(f"OpenRouter respondió {resp.status_code}: {detail}")

            async for line in resp.aiter_lines():
                if not line.startswith("data: "):
                    continue  # comentarios de keep-alive (": OPENROUTER PROCESSING")
                data = line[6:]
                if data == "[DONE]":
                    break
                chunk = json.loads(data)
                if "error" in chunk:
                    raise LLMError(chunk["error"].get("message", "Error del proveedor"))
                delta = chunk["choices"][0].get("delta", {}).get("content")
                if delta:
                    yield delta
