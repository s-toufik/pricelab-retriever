from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class BaseProvider:
    name: str
