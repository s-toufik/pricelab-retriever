from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI
from pricelab_core.infrastructure.http.middleware.request_id_middleware import RequestIDMiddleware
from pricelab_core.bootstrap.dependency_injection.logging import logger

from pricelab_retriever.bootstrap.container.container import Container


@asynccontextmanager
async def lifespan(app: FastAPI, container: Container) -> AsyncGenerator[None, None]:
    try:
        logger.info("Starting container ...")
        await container.start()
        yield
    except Exception as e:
        logger.error(f"Error starting container: {e}")
    finally:
        logger.info("Stopping container ...")
        await container.stop()


def create_app() -> FastAPI:
    container = Container()
    routers = []

    application = FastAPI(title="PriceLab Retriever", lifespan=lambda app: lifespan(app, container))

    routers.append(container.build_intraday_stock_router())
    for route in routers:
        application.include_router(route)

    application.add_middleware(RequestIDMiddleware)
    return application
