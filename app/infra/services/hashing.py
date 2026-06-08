import secrets

import bcrypt

from app.domain.hash_protocol import HashProtocol, HashableValue


class ServerHash(HashProtocol):
    @staticmethod
    def random_hash(lenb: int = 16) -> HashableValue: 
        token = secrets.token_urlsafe(lenb).encode()
        crypt = bcrypt.hashpw(token, bcrypt.gensalt())
        return HashableValue(crypt)
    
    @staticmethod
    def hash_value(value: HashableValue) -> HashableValue: 
        crypt = bcrypt.hashpw(value.bvalue, bcrypt.gensalt())
        return HashableValue(
            crypt
        )
    
    @staticmethod
    def compare_hash(raw_value: HashableValue, hash: HashableValue) -> bool:
        return bcrypt.checkpw(raw_value.bvalue, hash.bvalue)
    