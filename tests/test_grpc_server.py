import pytest
from unittest.mock import AsyncMock, patch
import app.proto.library_pb2 as library_pb2
import app.proto.library_pb2_grpc as library_pb2_grpc


@pytest.mark.asyncio
@patch("app.models.Member.create", new_callable=AsyncMock)
async def test_create_member(mock_get, mock_create, grpc_channel):
    mock_create.return_value.id = 1
    mock_get.return_value.email = "test@example.com"

    stub = library_pb2_grpc.LibraryServiceStub(grpc_channel)

    request = library_pb2.MemberRequest(
        first_name="Test",
        last_name="User",
        email="test@example.com",
        phone_number="1234567890",
        address="123 Street",
    )

    response = await stub.CreateMember(request)

    assert response.message == "Member created"
    assert response.id == 1

    mock_create.assert_awaited_once()
    mock_get.assert_awaited_once_with(id=1)
