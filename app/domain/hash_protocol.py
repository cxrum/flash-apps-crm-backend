from dataclasses import dataclass
from typing import Protocol

@dataclass(frozen=True)
class HashedValue:
    bvalue: bytes

    def to_hex(self) -> str:
        return self.bvalue.hex()
    
    def to_str(self) -> str:
        return self.bvalue.decode()
    
    @staticmethod
    def from_str(value: str) -> "HashedValue":
        return HashedValue(
            bvalue=value.encode()
        )
        
    @staticmethod
    def from_hex(hex_value: str) -> "HashedValue":
        return HashedValue(
            bvalue=int(hex_value, base=16).to_bytes()
        )
    
class HashProtocol(Protocol):
    
    @staticmethod
    def random_hash(lenb: int = 32) -> HashedValue: ... 
        
    @staticmethod
    def hash_value(value: HashedValue) -> HashedValue: ...
        
    @staticmethod
    def compare_hash(raw_value: HashedValue, hash: HashedValue) -> bool: ...
     