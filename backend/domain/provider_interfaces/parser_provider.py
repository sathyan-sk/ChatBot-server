"""Parser provider contract. Converts raw source bytes into a normalized,
structure-aware representation. Concrete parsers (document/html/structured/
plain-text) are selected by rag_engine/ingestion based on source type, but all
implement this same contract so the ingestion pipeline never branches on
vendor-specific logic."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class ParsedSection:
    title: str | None
    content: str
    order: int
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass
class ParsedDocument:
    sections: list[ParsedSection]
    source_metadata: dict[str, str] = field(default_factory=dict)


class ParserProviderInterface(ABC):
    @abstractmethod
    async def parse(self, raw_content: bytes, content_type: str) -> ParsedDocument:
        raise NotImplementedError

    @abstractmethod
    def supports(self, content_type: str) -> bool:
        """Whether this parser can handle the given content type. Used by the
        ingestion pipeline to select the correct parser without a hardcoded
        if/elif chain."""
        raise NotImplementedError
