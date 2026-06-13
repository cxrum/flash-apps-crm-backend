from dataclasses import dataclass


@dataclass(frozen=True)
class Money:
    base: str
    value: float
    rate_to_USD: float | None = None
    
    
    #TODO Make money base validation in this value class. Change money values to this class everywhere. 