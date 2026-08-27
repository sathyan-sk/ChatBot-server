# pdf_parser_provider.py
"""Requires pypdf: add "pypdf>=5.1.0" to pyproject.toml dependencies."""

import io

from pypdf import PdfReader

from domain.provider_interfaces.parser_provider import (
    ParsedDocument,
    ParsedSection,
    ParserProviderInterface,
)
from exceptions.domain_exceptions import ProviderError


class PdfParserProvider(ParserProviderInterface):
    async def parse(self, raw_content: bytes, content_type: str) -> ParsedDocument:
        try:
            reader = PdfReader(io.BytesIO(raw_content))
            sections = [
                ParsedSection(title=f"Page {i + 1}", content=page.extract_text() or "", order=i)
                for i, page in enumerate(reader.pages)
            ]
        except Exception as exc:
            raise ProviderError(f"Failed to parse PDF: {exc}") from exc
        return ParsedDocument(sections=sections)

    def supports(self, content_type: str) -> bool:
        return content_type == "application/pdf"
