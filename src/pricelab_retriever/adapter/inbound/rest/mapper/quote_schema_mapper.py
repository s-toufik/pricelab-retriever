from typing import Sequence, Iterator
from pricelab_core.domain.model.quotes.quote import Quote

from pricelab_retriever.adapter.inbound.rest.schema.quote_schema import QuoteSchema

class QuoteSchemaMapper:

    @staticmethod
    def map(source: Sequence[Quote]) -> Iterator[QuoteSchema]:
        for item in source:
            yield QuoteSchema(
                source=item.source,
                symbol=item.symbol,
                timestamp=item.timestamp,
                bid=item.bid,
                ask=item.ask,
                last=item.last,
                volume=item.volume
            )