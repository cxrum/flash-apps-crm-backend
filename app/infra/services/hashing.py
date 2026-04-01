import secrets

import bcrypt

from app.domain.hash_protocol import HashProtocol, HashedValue


class ServerHash(HashProtocol):
    @staticmethod
    def random_hash(lenb: int = 32) -> HashedValue: 
        token = secrets.token_urlsafe(lenb).encode()
        crypt = bcrypt.hashpw(token, bcrypt.gensalt())
        return HashedValue(crypt)
    
    @staticmethod
    def hash_value(value: HashedValue) -> HashedValue: 
        crypt = bcrypt.hashpw(value.bvalue, bcrypt.gensalt())
        return HashedValue(
            crypt
        )
    
    @staticmethod
    def compare_hash(raw_value: HashedValue, hash: HashedValue) -> bool:
        return bcrypt.checkpw(raw_value.bvalue, hash.bvalue)
    