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
        if not request.title or not request.author or not request.isbn:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Title, author and ISBN are required.")
            return library_pb2.BookResponse()

        existing = await models.Book.get_or_none(isbn=request.isbn)
        if existing:
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details("Book with same ISBN already exists.")
            return library_pb2.BookResponse()

        book = await models.Book.create(
            title=request.title, author=request.author, isbn=request.isbn
        )

        return library_pb2.BookResponse(
            id=book.id, message="Book created successfully."
        )

    async def BorrowBook(self, request, context):
        try:
            book = await models.Book.get_or_none(id=request.book_id)
            member = await models.Member.get_or_none(id=request.member_id)

            if not member:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Member not found.")
                return library_pb2.BorrowResponse()

            if not book:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Book not found.")
                return library_pb2.BorrowResponse()

            if not book.available:
                context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
                context.set_details("Book is already borrowed.")
                return library_pb2.BorrowResponse()

            await models.Borrow.create(member=member, book=book)
            book.available = False
            await book.save()

            return library_pb2.BorrowResponse(message="Book borrowed successfully.")
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Unexpected error: {str(e)}")
            return library_pb2.BorrowResponse()

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
            borrows = await models.Borrow.filter(return_date=None).prefetch_related(
                "book"
            )[
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
