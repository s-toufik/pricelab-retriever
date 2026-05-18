from fastapi import FastAPI

from pricelab_retriever.bootstrap.startup.create_application import create_app

app: FastAPI = create_app()
