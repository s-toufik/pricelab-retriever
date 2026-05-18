from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI
from pricelab_core.infrastructure.http.middleware.request_id_middleware import RequestIDMiddleware

from pricelab_retriever.bootstrap.container import Container


def create_app() -> FastAPI:
    container = Container()

    @asynccontextmanager
    async def lifespan(fast_api_app: FastAPI) -> AsyncGenerator[None, None]:
        await container.start()
        yield
        await container.stop()

    application = FastAPI(title="PriceLab Retriever", lifespan=lifespan)
    intraday_controller = container.build_intraday_stock_controller()

    application.include_router(intraday_controller.router)
    application.add_middleware(RequestIDMiddleware)
    return application
