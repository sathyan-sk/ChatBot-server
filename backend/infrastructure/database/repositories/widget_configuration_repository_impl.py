from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.widget_configuration import WidgetConfiguration
from domain.repository_interfaces.widget_configuration_repository import (
    WidgetConfigurationRepositoryInterface,
)
from infrastructure.database.models.widget_configuration_model import (
    WidgetConfigurationModel,
)


def _to_entity(model: WidgetConfigurationModel) -> WidgetConfiguration:
    return WidgetConfiguration(
        id=model.id,
        application_id=model.application_id,
        allowed_origins=list(model.allowed_origins or []),
        theme_color=model.theme_color,
        welcome_message=model.welcome_message,
        launcher_label=model.launcher_label,
    )


class WidgetConfigurationRepository(WidgetConfigurationRepositoryInterface):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, config: WidgetConfiguration) -> WidgetConfiguration:
        model = WidgetConfigurationModel(
            id=config.id,
            application_id=config.application_id,
            allowed_origins=config.allowed_origins,
            theme_color=config.theme_color,
            welcome_message=config.welcome_message,
            launcher_label=config.launcher_label,
        )
        self._session.add(model)
        await self._session.flush()
        return _to_entity(model)

    async def get_by_application_id(self, application_id: str) -> WidgetConfiguration | None:
        result = await self._session.execute(
            select(WidgetConfigurationModel).where(
                WidgetConfigurationModel.application_id == application_id
            )
        )
        model = result.scalar_one_or_none()
        return _to_entity(model) if model else None

    async def update(self, config: WidgetConfiguration) -> WidgetConfiguration:
        result = await self._session.execute(
            select(WidgetConfigurationModel).where(
                WidgetConfigurationModel.application_id == config.application_id
            )
        )
        model = result.scalar_one()
        model.allowed_origins = config.allowed_origins
        model.theme_color = config.theme_color
        model.welcome_message = config.welcome_message
        model.launcher_label = config.launcher_label
        await self._session.flush()
        return _to_entity(model)
