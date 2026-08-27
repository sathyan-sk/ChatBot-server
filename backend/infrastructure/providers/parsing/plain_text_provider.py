# plain_text_parser_provider.py
from domain.provider_interfaces.parser_provider import (
    ParsedDocument,
    ParsedSection,
    ParserProviderInterface,
)


class PlainTextParserProvider(ParserProviderInterface):
    async def parse(self, raw_content: bytes, content_type: str) -> ParsedDocument:
        text = raw_content.decode("utf-8", errors="replace")
        return ParsedDocument(sections=[ParsedSection(title=None, content=text, order=0)])

    def supports(self, content_type: str) -> bool:
        return content_type in ("text/plain",)
