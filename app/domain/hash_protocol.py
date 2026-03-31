from typing import Protocol


class HashProtocol(Protocol):
    
    @staticmethod
    def random_hash(lenb: int = 32) -> str: ... 
        
    @staticmethod
    def hash_value(value: str) -> str: ...
        
    @staticmethod
    def compare_hash(raw_value:str, hash: str) -> bool: ...
     