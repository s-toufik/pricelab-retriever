from typing import TypeVar, Protocol, Iterator, Sequence

S = TypeVar("S")
T = TypeVar("T")


class SchemaMapper(Protocol[S, T]):
    def map(self, source: Sequence[S]) -> Iterator[T]: ...
