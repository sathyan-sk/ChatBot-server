"""OpenRouter LLM provider. Model is passed per-request (LLMGenerationRequest.model),
never hardcoded here — provider identity and model choice are independent axes."""

import httpx

from domain.provider_interfaces.llm_provider import (
    LLMGenerationRequest,
    LLMGenerationResult,
    LLMProviderInterface,
)
from exceptions.domain_exceptions import ProviderError

_OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


class OpenRouterLLMProvider(LLMProviderInterface):
    def __init__(self, api_key: str, timeout_seconds: float = 30.0) -> None:
        self._api_key = api_key
        self._timeout = timeout_seconds

    async def generate(self, request: LLMGenerationRequest) -> LLMGenerationResult:
        payload = {
            "model": request.model,
            "messages": [{"role": t.role, "content": t.content} for t in request.messages],
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
        }
        headers = {"Authorization": f"Bearer {self._api_key}", "Content-Type": "application/json"}
        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                response = await client.post(_OPENROUTER_URL, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
        except httpx.HTTPError as exc:
            raise ProviderError(f"OpenRouter request failed: {exc}") from exc

        try:
            choice = data["choices"][0]
            content = choice["message"]["content"]
            finish_reason = choice.get("finish_reason", "stop")
            usage = data.get("usage", {})
        except (KeyError, IndexError) as exc:
            raise ProviderError(f"OpenRouter returned an unexpected response shape: {exc}") from exc

        return LLMGenerationResult(
            content=content,
            model=request.model,
            finish_reason=finish_reason,
            prompt_tokens=usage.get("prompt_tokens"),
            completion_tokens=usage.get("completion_tokens"),
        )

    async def health_check(self) -> bool:
        headers = {"Authorization": f"Bearer {self._api_key}"}
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get("https://openrouter.ai/api/v1/models", headers=headers)
                return response.status_code == 200
        except httpx.HTTPError:
            return False
