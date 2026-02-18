from enum import Enum
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.errors import AppError
from app.api.v1.handlers.orders import router as orders_router
from app.api.v1.handlers.products import router as products_router
from app.grpc.clients.user_client import UserClient


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.user_client = UserClient("localhost:50051")
    yield 

    await app.state.user_client.close()


app = FastAPI(lifespan=lifespan)


@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    code = exc.code.value if isinstance(exc.code, Enum) else exc.code

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": code,
            "message": exc.message,
            "details": exc.details if exc.details else "no details"
        }
    )


app.include_router(orders_router)
app.include_router(products_router)

@app.on_event("shutdown")
async def shutdown():
    await app.state.user_client.close()