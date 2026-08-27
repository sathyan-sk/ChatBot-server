"""Storage provider contract. Abstracts Supabase Storage / S3 so
DataSourceService and the ingestion file_loader never call a vendor SDK
directly."""

from abc import ABC, abstractmethod


class StorageProviderInterface(ABC):
    @abstractmethod
    async def upload(self, path: str, content: bytes, content_type: str) -> str:
        """Uploads content and returns the durable storage_path. Callers must
        validate the returned path is non-null before persisting a DataSource
        row (Storage Validator cautionary rule)."""
        raise NotImplementedError

    @abstractmethod
    async def download(self, path: str) -> bytes:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, path: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_signed_url(self, path: str, expires_in_seconds: int = 3600) -> str:
        raise NotImplementedError

    @abstractmethod
    async def health_check(self) -> bool:
        raise NotImplementedError
