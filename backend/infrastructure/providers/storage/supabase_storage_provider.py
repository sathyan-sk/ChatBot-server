"""Supabase Storage provider. Uses the supabase-py client with the
service_role key configured in .env — never the anon key."""

from supabase import Client, create_client

from domain.provider_interfaces.storage_provider import StorageProviderInterface
from exceptions.domain_exceptions import ProviderError


class SupabaseStorageProvider(StorageProviderInterface):
    def __init__(self, supabase_url: str, supabase_key: str, bucket: str) -> None:
        self._client: Client = create_client(supabase_url, supabase_key)
        self._bucket = bucket

    async def upload(self, path: str, content: bytes, content_type: str) -> str:
        try:
            self._client.storage.from_(self._bucket).upload(
                path, content, {"content-type": content_type, "upsert": "true"}
            )
        except Exception as exc:
            raise ProviderError(f"Supabase upload failed: {exc}") from exc
        return path

    async def download(self, path: str) -> bytes:
        try:
            return self._client.storage.from_(self._bucket).download(path)
        except Exception as exc:
            raise ProviderError(f"Supabase download failed: {exc}") from exc

    async def delete(self, path: str) -> None:
        try:
            self._client.storage.from_(self._bucket).remove([path])
        except Exception as exc:
            raise ProviderError(f"Supabase delete failed: {exc}") from exc

    async def get_signed_url(self, path: str, expires_in_seconds: int = 3600) -> str:
        try:
            result = self._client.storage.from_(self._bucket).create_signed_url(
                path, expires_in_seconds
            )
            signed_url = result.get("signedURL")
            if signed_url is None:
                raise ProviderError("Supabase returned no signed URL")
            return signed_url
        except Exception as exc:
            raise ProviderError(f"Supabase signed URL generation failed: {exc}") from exc

    async def health_check(self) -> bool:
        try:
            self._client.storage.from_(self._bucket).list()
            return True
        except Exception:
            return False
