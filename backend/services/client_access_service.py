from __future__ import annotations

from domain.entities.application_context import ApplicationContext

from domain.repository_interfaces.application_credential_repository import (
    ApplicationCredentialRepositoryInterface,
)
from domain.repository_interfaces.knowledge_base_repository import (
    KnowledgeBaseRepositoryInterface,
)
from exceptions.domain_exceptions import ForbiddenError, UnauthorizedError


class ClientAccessService:
    """Resolves a client API key to an ApplicationContext.

    API key -> ApplicationCredential -> KnowledgeBase -> ApplicationContext
    """

    def __init__(
        self,
        credential_repository: ApplicationCredentialRepositoryInterface,
        knowledge_base_repository: KnowledgeBaseRepositoryInterface,
    ) -> None:
        self._credential_repository = credential_repository
        self._knowledge_base_repository = knowledge_base_repository

    async def resolve_application_context(self, api_key_hash: str) -> ApplicationContext:
        credential = await self._credential_repository.get_by_api_key_hash(api_key_hash)
        if credential is None:
            raise UnauthorizedError("Invalid API key.")

        knowledge_base = await self._knowledge_base_repository.get_by_application_id(
            credential.application_id
        )
        if knowledge_base is None:
            raise ForbiddenError("Knowledge base is not configured for this application.")

        return ApplicationContext(
            application_id=credential.application_id,
            knowledge_base_id=knowledge_base.id,
        )
