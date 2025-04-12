import asyncio
import grpc
from app import models
from app.database import TORTOISE_ORM
from tortoise import Tortoise
from app.proto import library_pb2, library_pb2_grpc


class LibraryServiceServicer(library_pb2_grpc.LibraryServiceServicer):
    async def CreateMember(self, request, context):
        member = await models.Member.create(
            first_name=request.first_name,
            last_name=request.last_name,
            email=request.email,
            phone_number=request.phone_number,
            address=request.address,
        )
        return library_pb2.MemberResponse(id=member.id, message="Member created")
 
async def serve():
    await Tortoise.init(config=TORTOISE_ORM)
    server = grpc.aio.server()
    library_pb2_grpc.add_LibraryServiceServicer_to_server(LibraryServiceServicer(), server)
    server.add_insecure_port("[::]:50051")
    await server.start()
    print("gRPC server started on port 50051")
    await server.wait_for_termination()

if __name__ == "__main__":
    print("Starting gRPC server...")
    asyncio.run(serve())

