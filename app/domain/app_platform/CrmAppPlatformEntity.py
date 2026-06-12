from __future__ import annotations

import re
from copy import copy
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from app.application.contracts.encryption import EncryptionServiceProtocol
from app.domain.exceptions import PlatformDoestExist, PlatformInstallKeyMustBeUniqPerApp, PlatformStatusDoestExist
from app.domain.hash_protocol import HashProtocol
from app.domain.role.CrmRoleEntity import CrmRoleEntity, Roles


@dataclass
class VersionPolicyEntity:
    current_version: str | None = None
    min_version: str | None = None
    max_version: str | None = None
    allowed_versions: list[str] = field(default_factory=list)
    blocked_versions: list[str] = field(default_factory=list)
    required: bool = False

    @staticmethod
    def _version_parts(value: str) -> tuple[int, ...]:
        numbers = [int(item) for item in re.findall(r"\d+", value)]
        return tuple(numbers or [0])

    @classmethod
    def normalize_version(cls, version: str | None) -> str | None:
        if version is None:
            return None

        version_text = str(version).strip()
        version_parts = cls._version_parts(version_text)
        if version_parts == (0,) and not re.search(r"\d", version_text):
            return version_text

        return ".".join(str(part) for part in version_parts)

    @classmethod
    def normalize_version_list(cls, value: Any) -> list[str]:
        if value is None:
            return []
        if isinstance(value, str):
            normalized = cls.normalize_version(value)
            return [] if normalized is None else [normalized]
        if isinstance(value, list | tuple | set):
            return [normalized for item in value if (normalized := cls.normalize_version(str(item))) is not None]
        return []

    @classmethod
    def create(
        cls,
        *,
        current_version: str | None = None,
        min_version: str | None = None,
        max_version: str | None = None,
        allowed_versions: list[str] | None = None,
        blocked_versions: list[str] | None = None,
        required: bool = False,
    ) -> "VersionPolicyEntity":
        return cls(
            current_version=cls.normalize_version(current_version),
            min_version=cls.normalize_version(min_version),
            max_version=cls.normalize_version(max_version),
            allowed_versions=cls.normalize_version_list(allowed_versions),
            blocked_versions=cls.normalize_version_list(blocked_versions),
            required=required,
        )

    @classmethod
    def create_from_dict(cls, data: dict[str, Any]) -> "VersionPolicyEntity":
        return cls.create(
            current_version=data.get("current_version") or data.get("current"),
            min_version=data.get("min_version") or data.get("min"),
            max_version=data.get("max_version") or data.get("max"),
            allowed_versions=(
                data.get("allowed_versions")
                or data.get("supported_versions")
                or data.get("allowed_version")
                or data.get("allowed")
            ),
            blocked_versions=(
                data.get("blocked_versions")
                or data.get("unsupported_versions")
                or data.get("blocked_version")
                or data.get("blocked")
            ),
            required=bool(data.get("required", False)),
        )

    @classmethod
    def from_value(cls, value: "VersionPolicyEntity | dict[str, Any] | None") -> "VersionPolicyEntity | None":
        if value is None:
            return None
        if isinstance(value, VersionPolicyEntity):
            return value
        return cls.create_from_dict(value)

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {"required": self.required}
        if self.current_version is not None:
            data["current_version"] = self.current_version
        if self.min_version is not None:
            data["min_version"] = self.min_version
        if self.max_version is not None:
            data["max_version"] = self.max_version
        if self.allowed_versions:
            data["allowed_versions"] = list(self.allowed_versions)
        if self.blocked_versions:
            data["blocked_versions"] = list(self.blocked_versions)
        return data


@dataclass
class CrmAppPlatformEntity:
    app_id: int
    platform: str
    package_name: str
    install_key: str
    sdk_secret_encrypted: str
    sdk_public_key: str
    current_version: str
    version_policy: VersionPolicyEntity | None = None
    sdk_secret_fallback_encrypted: str | None = None
    store_url: str | None = None
    status: str = "active"
    platform_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    _sdk_secret_plain: str | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        self.current_version = VersionPolicyEntity.normalize_version(self.current_version) or self.current_version
        self.version_policy = VersionPolicyEntity.from_value(self.version_policy)

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

    def version_policy_dict(self) -> dict[str, Any] | None:
        if self.version_policy is None:
            return None
        return self.version_policy.to_dict()

    def version_control_dict(self) -> dict[str, Any]:
        version_policy = self.version_policy or VersionPolicyEntity()
        data = version_policy.to_dict()
        data["current_version"] = self.current_version
        return data

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
        self.sdk_secret_encrypted = encryption.encrypt(source_secret)  # type: ignore
        self._sdk_secret_plain = None

    def secret_view_for_role(self, user_role: Roles | str | None = None) -> str:
        if CrmRoleEntity.normalize_role(user_role) is Roles.ADMIN:  # type: ignore
            return self.sdk_secret_encrypted
        return self._mask_secret(self.sdk_secret_encrypted)

    def rotate_secret(self, hasher: HashProtocol, encryption: EncryptionServiceProtocol) -> str:
        self.sdk_secret_fallback_encrypted = copy(self.sdk_secret_encrypted)
        self.create_secret(hasher)
        self.encrypt_secret(encryption)
        return self.sdk_secret_fallback_encrypted

    def uniq_per_app(self, platforms: list[CrmAppPlatformEntity]):
        for platform in platforms:
            if platform.install_key == self.install_key:
                raise PlatformInstallKeyMustBeUniqPerApp(self.install_key)

    @staticmethod
    def create(
        *,
        hasher: HashProtocol,
        app_id: int,
        platform: str,
        package_name: str,
        install_key: str,
        current_version: str,
        version_policy: VersionPolicyEntity | dict[str, Any] | None = None,
        store_url: str | None = None,
        status: str = "inactive",
    ) -> "CrmAppPlatformEntity":
        secret_plain = hasher.random_hash(CrmAppPlatformEntity.__sdk_secret_blen()).to_hex()
        sdk_public_key = hasher.random_hash(CrmAppPlatformEntity.__sdk_secret_blen()).to_hex()

        if platform not in CrmAppPlatformEntity.__available_platforms():
            raise PlatformDoestExist(platform)

        if status not in CrmAppPlatformEntity.__available_statuses():
            raise PlatformStatusDoestExist(status)

        return CrmAppPlatformEntity(
            app_id=app_id,
            platform=platform,
            package_name=package_name,
            install_key=install_key,
            store_url=store_url,
            sdk_public_key=sdk_public_key,
            current_version=current_version,
            version_policy=VersionPolicyEntity.from_value(version_policy),
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
        current_version: str | None = None,
        version_policy: VersionPolicyEntity | dict[str, Any] | None = None,
        status: str | None = None,
    ) -> None:
        normalized_version = VersionPolicyEntity.normalize_version(current_version)

        self.app_id = app_id if app_id is not None else self.app_id
        self.platform = platform if platform is not None and platform in self.__available_platforms() else self.platform
        self.package_name = package_name if package_name is not None else self.package_name
        self.install_key = install_key if install_key is not None else self.install_key
        self.sdk_secret_encrypted = (
            sdk_secret_encrypted if sdk_secret_encrypted is not None else self.sdk_secret_encrypted
        )
        self.store_url = store_url if store_url is not None else self.store_url
        self.sdk_public_key = sdk_public_key if sdk_public_key is not None else self.sdk_public_key
        self.current_version = self.current_version if normalized_version is None else normalized_version

        self.version_policy = (
            VersionPolicyEntity.from_value(version_policy) if version_policy is not None else self.version_policy
        )

        self.status = status if status is not None and status in self.__available_statuses() else self.status

        self.updated_at = datetime.now(UTC)
