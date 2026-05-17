from fastapi import FastAPI

from pricelab_retriever.adapter.inbound.rest.create_application import create_app

app: FastAPI = create_app()
