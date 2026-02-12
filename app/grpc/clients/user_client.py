import grpc
from uuid import UUID
from starlette.status import HTTP_504_GATEWAY_TIMEOUT, HTTP_503_SERVICE_UNAVAILABLE, HTTP_502_BAD_GATEWAY

import app.grpc.generated.user_service_pb2 as user_pb2
import app.grpc.generated.user_service_pb2_grpc as user_pb2_grpc
from app.core.errors import AppError
from app.utils.error_codes import ErrorCode


class UserClient:
    def __init__(self, target: str):
        self._channel = grpc.aio.insecure_channel(target)
        self._stub = user_pb2_grpc.UserServiceStub(self._channel)

    async def validate_user(
        self,
        *,
        telegram_id: int,
        phone: str = "",
        full_name: str = ""
    ) -> UUID:

        request = user_pb2.ValidateUserRequest(
            telegram_id=telegram_id,
            phone=phone,
            full_name=full_name
        )

        try:
            resp = await self._stub.ValidateTelegramUser(request, timeout=2.0)
        except grpc.aio.AioRpcError as e:
            if e.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
                raise AppError(
                    message="User service timeout.",
                    code=ErrorCode.USER_SVC_TIMEOUT,
                    status_code=HTTP_504_GATEWAY_TIMEOUT
                )
            if e.code() in (grpc.StatusCode.UNAVAILABLE, grpc.StatusCode.RESOURCE_EXHAUSTED):
                raise AppError(
                    message="User service unuvailable.",
                    code=ErrorCode.USER_SVC_UNAVAILABLE,
                    status_code=HTTP_503_SERVICE_UNAVAILABLE
                )
            raise AppError(
                message="User Service Error.",
                code=ErrorCode.USER_SVC_ERROR,
                status_code=HTTP_502_BAD_GATEWAY
            )


        if resp.status != user_pb2.VALID:
            raise ValueError("User validation failed")

        return UUID(resp.user_id)

    async def close(self):
        await self._channel.close()
