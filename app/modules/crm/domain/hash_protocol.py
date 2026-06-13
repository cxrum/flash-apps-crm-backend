from dataclasses import dataclass
from typing import Protocol

@dataclass(frozen=True)
class HashableValue:
    bvalue: bytes

    def to_hex(self) -> str:
        return self.bvalue.hex()
    
    def to_str(self) -> str:
        return self.bvalue.decode()
    
    @staticmethod
    def from_str(value: str) -> "HashableValue":
        return HashableValue(
            bvalue=value.encode()
        )
        
    @staticmethod
    def from_hex(hex_value: str) -> "HashableValue":
        return HashableValue(
            bvalue=bytes.fromhex(hex_value)
        )
    
class HashProtocol(Protocol):
    
    @staticmethod
    def random_hash(lenb: int = 32) -> HashableValue: ... 
        
    @staticmethod
    def hash_value(value: HashableValue) -> HashableValue: ...
        
    @staticmethod
    def compare_hash(raw_value: HashableValue, hash: HashableValue) -> bool: ...
     
