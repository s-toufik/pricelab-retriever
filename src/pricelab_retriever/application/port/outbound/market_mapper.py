from typing import Protocol, TypeVar, Iterator, runtime_checkable

S = TypeVar("S")
T = TypeVar("T")


@runtime_checkable
class MarketMapper(Protocol[S, T]):
    def map(self, source: S) -> Iterator[T]: ...
