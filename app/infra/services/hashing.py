import secrets

import bcrypt

from app.domain.hash_protocol import HashProtocol


class ServerHash(HashProtocol):
    @staticmethod
    def random_hash(lenb: int = 32) -> str: 
        token = secrets.token_urlsafe(lenb).encode()
        crypt = bcrypt.hashpw(token, bcrypt.gensalt())
        return crypt.decode()
    
    @staticmethod
    def hash_value(value: str) -> str: 
        crypt = bcrypt.hashpw(value.encode(), bcrypt.gensalt())
        return crypt.decode()
    
    @staticmethod
    def compare_hash(raw_value:str, hash: str) -> bool:
        return bcrypt.checkpw(raw_value.encode(), hash.encode())
    