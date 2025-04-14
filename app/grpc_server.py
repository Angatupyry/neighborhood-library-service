import asyncio
import grpc
from app import models
from app.database import TORTOISE_ORM
from tortoise import Tortoise
from app.proto import library_pb2, library_pb2_grpc
from datetime import datetime


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

    async def CreateBook(self, request, context):
        book = await models.Book.create(
            title=request.title, author=request.author, isbn=request.isbn
        )
        return library_pb2.BookResponse(id=book.id, message="Book created")

    async def BorrowBook(self, request, context):
        book = await models.Book.get(id=request.book_id)
        if not book.available:
            context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
            context.set_details("Book not available")
            return library_pb2.BorrowResponse()
        borrow = await models.Borrow.create(
            member_id=request.member_id, book_id=request.book_id
        )
        book.available = False
        await book.save()
        return library_pb2.BorrowResponse(id=borrow.id, message="Book borrowed")

    async def ReturnBook(self, request, context):
        borrow = await models.Borrow.get(id=request.borrow_id).prefetch_related("book")
        borrow.return_date = datetime.now()
        await borrow.save()
        borrow.book.available = True
        await borrow.book.save()
        return library_pb2.ReturnResponse(message="Book returned")


async def ListBorrowedBooks(self, request, context):
    if request.member_id:
        borrows = await models.Borrow.filter(
            member_id=request.member_id, return_date=None
        ).prefetch_related("book")
    else:
        borrows = await models.Borrow.filter(return_date=None).prefetch_related("book")[
            :20
        ]  # Limit to the first 20 results
    books = [
        library_pb2.BorrowedBook(
            book_id=borrow.book.id,
            title=borrow.book.title,
            author=borrow.book.author,
            borrow_date=borrow.borrow_date.isoformat(),
        )
        for borrow in borrows
    ]

    return library_pb2.ListBorrowedResponse(books=books)


async def serve():
    await Tortoise.init(config=TORTOISE_ORM)
    server = grpc.aio.server()
    library_pb2_grpc.add_LibraryServiceServicer_to_server(
        LibraryServiceServicer(), server
    )
    server.add_insecure_port("[::]:50051")
    await server.start()
    print("gRPC server started on port 50051")
    await server.wait_for_termination()


if __name__ == "__main__":
    print("Starting gRPC server...")
    asyncio.run(serve())
