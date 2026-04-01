from app.application.contracts.encryption import EncryptionServiceProtocol


class EncryptionService(EncryptionServiceProtocol):
    def encrypt(self, value: str) -> str:
        raise NotImplementedError
    
    def decrypt(self, value: str) -> str:
        raise NotImplementedError