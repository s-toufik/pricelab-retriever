from typing import Protocol, TypeVar, Iterator

S = TypeVar('S')
T = TypeVar('T')

class MarketDataMapper(Protocol[S, T]):
    def map(self, source: S) -> Iterator[T]: ...