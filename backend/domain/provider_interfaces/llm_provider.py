"""LLM provider contract. Provider = which service executes generation.
Model = which model that provider runs — passed as a parameter, never baked
into the provider implementation's identity."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class ChatTurn:
    role: str  # "system" | "user" | "assistant"
    content: str


@dataclass
class LLMGenerationRequest:
    model: str
    messages: list[ChatTurn]
    temperature: float = 0.2
    max_tokens: int = 800
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass
class LLMGenerationResult:
    content: str
    model: str
    finish_reason: str
    prompt_tokens: int | None = None
    completion_tokens: int | None = None


class LLMProviderInterface(ABC):
    @abstractmethod
    async def generate(self, request: LLMGenerationRequest) -> LLMGenerationResult:
        """Execute a single grounded-generation call. Must raise
        exceptions.domain_exceptions.ProviderError on failure — never a raw
        vendor SDK exception."""
        raise NotImplementedError

    @abstractmethod
    async def health_check(self) -> bool:
        """Cheap connectivity check. Never called on the hot request path —
        used only by the admin-only diagnostics endpoint."""
        raise NotImplementedError
