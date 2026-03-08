

class PlatformUseCases:
    @staticmethod
    def is_supported_platform(platform: str) -> bool:
        return platform in {"android", "ios"}