import asyncio, grpc

from app.core.config import get_settings
from app.database.db import async_session_maker
from app.api.v1.deps.grpc import uow_factory
from app.grpc.handlers.drafts import OrderServiceGrpc
import app.grpc.generated.order_draft_pb2_grpc as order_pb2_grpc

async def run_grpc_server() -> None:
    settings = get_settings()
    server = grpc.aio.server()


    order_pb2_grpc.add_OrderServiceServicer_to_server(
        OrderServiceGrpc(uow_factory),
        server
    )

    server.add_insecure_port(f"[::]:{settings.grpc_port}")
    await server.start()
    print("🚀 Order gRPC server running on 50052")
    
    try:
        await server.wait_for_termination()
    except asyncio.CancelledError:
        print("🛑 gRPC server stopped")