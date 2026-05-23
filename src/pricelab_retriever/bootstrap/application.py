from fastapi import FastAPI

from pricelab_retriever.bootstrap.container.create_application import create_app

app: FastAPI = create_app()
