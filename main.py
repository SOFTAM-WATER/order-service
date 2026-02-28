import asyncio
from enum import Enum
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.errors import AppError
from app.grpc.server import run_grpc_server
from scripts.init_models import init_models
from app.database.db import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    grpc_task = asyncio.create_task(run_grpc_server())    
    await init_models(engine)
    
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

@app.on_event("shutdown")
async def shutdown():
    await app.state.user_client.close()