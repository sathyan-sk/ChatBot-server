from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.application_credential import ApplicationCredential, CredentialStatus
from domain.repository_interfaces.application_credential_repository import (
    ApplicationCredentialRepositoryInterface,
)
from infrastructure.database.models.application_credential_model import (
    ApplicationCredentialModel,
)


def _to_entity(model: ApplicationCredentialModel) -> ApplicationCredential:
    return ApplicationCredential(
        id=model.id,
        application_id=model.application_id,
        api_key_hash=model.api_key_hash,
        widget_key=model.widget_key,
        status=CredentialStatus(model.status),
        created_at=model.created_at,
        revoked_at=model.revoked_at,
    )


class ApplicationCredentialRepository(ApplicationCredentialRepositoryInterface):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, credential: ApplicationCredential) -> ApplicationCredential:
        model = ApplicationCredentialModel(
            id=credential.id,
            application_id=credential.application_id,
            api_key_hash=credential.api_key_hash,
            widget_key=credential.widget_key,
            status=credential.status.value,
            created_at=credential.created_at,
        )
        self._session.add(model)
        await self._session.flush()
        return _to_entity(model)

    async def get_by_api_key_hash(self, api_key_hash: str) -> ApplicationCredential | None:
        result = await self._session.execute(
            select(ApplicationCredentialModel).where(
                ApplicationCredentialModel.api_key_hash == api_key_hash,
                ApplicationCredentialModel.status == CredentialStatus.ACTIVE.value,
            )
        )
        model = result.scalar_one_or_none()
        return _to_entity(model) if model else None

    async def get_by_widget_key(self, widget_key: str) -> ApplicationCredential | None:
        result = await self._session.execute(
            select(ApplicationCredentialModel).where(
                ApplicationCredentialModel.widget_key == widget_key,
                ApplicationCredentialModel.status == CredentialStatus.ACTIVE.value,
            )
        )
        model = result.scalar_one_or_none()
        return _to_entity(model) if model else None

    async def list_by_application(self, application_id: str) -> list[ApplicationCredential]:
        result = await self._session.execute(
            select(ApplicationCredentialModel).where(
                ApplicationCredentialModel.application_id == application_id
            )
        )
        return [_to_entity(m) for m in result.scalars().all()]

    async def revoke(self, credential_id: str) -> None:
        from datetime import UTC, datetime

        result = await self._session.execute(
            select(ApplicationCredentialModel).where(ApplicationCredentialModel.id == credential_id)
        )
        model = result.scalar_one()
        model.status = CredentialStatus.REVOKED.value
        model.revoked_at = datetime.now(UTC)
        await self._session.flush()
