from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.routers.transaction_router import transaction_router


def create_app():
    app = FastAPI(title="Export File Parser Service")

    origins = ["*"]

    # See https://fastapi.tiangolo.com/tutorial/cors/
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(transaction_router, prefix="")

    return app
