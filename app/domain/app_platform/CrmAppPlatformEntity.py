from __future__ import annotations

from copy import copy
from dataclasses import dataclass, field
from datetime import UTC, datetime

from app.application.contracts.encryption import EncryptionServiceProtocol
from app.domain.hash_protocol import HashProtocol
from app.domain.role.CrmRoleEntity import CrmRoleEntity, Roles


@dataclass
class CrmAppPlatformEntity:
    app_id: int
    platform: str
    package_name: str
    install_key: str
    sdk_secret_encrypted: str
    sdk_public_key: str
    sdk_secret_fallback_encrypted: str | None = None
    store_url: str | None = None
    status: str = "active"
    platform_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    _sdk_secret_plain: str | None = field(default=None, repr=False, compare=False)

    @classmethod
    def __sdk_secret_blen(cls) -> int:
        return 8

    @staticmethod
    def __available_statuses() -> list[str]:
        return ["active", "inactive"]

    @staticmethod
    def __available_platforms() -> list[str]:
        return ["android", "ios"]

    @staticmethod
    def _mask_secret(value: str) -> str:
        if len(value) <= 3:
            return "***"
        return value[:3] + "***"

    def is_valid_platform(self) -> bool:
        return self.platform in CrmAppPlatformEntity.__available_platforms()

    def is_valid_status(self) -> bool:
        return self.status in CrmAppPlatformEntity.__available_statuses()

    def activate(self):
        self.status = "active"
        self.updated_at = datetime.now()

    def deactivate(self):
        self.status = "inactive"
        self.updated_at = datetime.now()

    def create_secret(self, hasher: HashProtocol) -> None:
        self._sdk_secret_plain = hasher.random_hash(self.__sdk_secret_blen()).to_hex()

    def encrypt_secret(self, encryption: EncryptionServiceProtocol) -> None:
        source_secret = self._sdk_secret_plain
        self.sdk_secret_encrypted = encryption.encrypt(source_secret)
        self._sdk_secret_plain = None

    def secret_view_for_role(self, user_role: Roles | str | None = None) -> str:
        if CrmRoleEntity.normalize_role(user_role) is Roles.ADMIN:
            return self.sdk_secret_encrypted
        return self._mask_secret(self.sdk_secret_encrypted)

    def rotate_secret(self, hasher: HashProtocol, encryption: EncryptionServiceProtocol):
        self.sdk_secret_fallback_encrypted = copy(self.sdk_secret_encrypted)
        self.create_secret(hasher)
        self.encrypt_secret(encryption)

    @staticmethod
    def create(
        *,
        hasher: HashProtocol,
        app_id: int,
        platform: str,
        package_name: str,
        install_key: str,
        store_url: str | None = None,
        status: str = "active",
    ) -> "CrmAppPlatformEntity":
        secret_plain = hasher.random_hash(CrmAppPlatformEntity.__sdk_secret_blen()).to_hex()
        sdk_public_key = hasher.random_hash(CrmAppPlatformEntity.__sdk_secret_blen()).to_hex()
        return CrmAppPlatformEntity(
            app_id=app_id,
            platform=platform,
            package_name=package_name,
            install_key=install_key,
            store_url=store_url,
            sdk_public_key=sdk_public_key,
            status=status,
            sdk_secret_encrypted="",
            _sdk_secret_plain=secret_plain,
        )

    def update(
        self,
        *,
        app_id: int | None = None,
        platform: str | None = None,
        package_name: str | None = None,
        install_key: str | None = None,
        sdk_secret_encrypted: str | None = None,
        store_url: str | None = None,
        sdk_public_key: str | None = None,
        status: str | None = None,
        is_active: bool | None = None,
    ) -> None:
        self.app_id = app_id if app_id is not None else self.app_id
        self.platform = platform if platform is not None else self.platform
        self.package_name = package_name if package_name is not None else self.package_name
        self.install_key = install_key if install_key is not None else self.install_key
        self.sdk_secret_encrypted = (
            sdk_secret_encrypted if sdk_secret_encrypted is not None else self.sdk_secret_encrypted
        )
        self.store_url = store_url if store_url is not None else self.store_url
        self.sdk_public_key = sdk_public_key if sdk_public_key is not None else self.sdk_public_key
        self.status = status if status is not None else self.status

        if is_active is not None:
            self.status = "active" if is_active else "inactive"

        self.updated_at = datetime.now(UTC)
