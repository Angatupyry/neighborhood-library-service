import asyncio
import grpc
import random
from uuid import uuid4
from app.proto import library_pb2, library_pb2_grpc


def generate_random_member():
    uid = uuid4().hex[:6]
    return library_pb2.MemberRequest(
        first_name=f"TestFirst{uid}",
        last_name=f"TestLast{uid}",
        email=f"user{uid}@example.com",
        phone_number=str(random.randint(1000000000, 9999999999)),
        address=f"{random.randint(1, 999)} Random Street",
    )


def generate_random_book():
    uid = uuid4().hex[:6]
    return library_pb2.BookRequest(
        title=f"Test Book {uid}",
        author=f"Author {uid}",
        isbn=str(random.randint(1000000000000, 9999999999999)),
    )


async def main():
    async with grpc.aio.insecure_channel("grpc_server:50051") as channel:
        stub = library_pb2_grpc.LibraryServiceStub(channel)

        # Create dynamic Member
        member_request = generate_random_member()
        member_response = await stub.CreateMember(member_request)
        member_id = member_response.id
        print(f"Member created: ID = {member_id}, message: {member_response.message}")

        # Create dynamic Book
        book_request = generate_random_book()
        book_response = await stub.CreateBook(book_request)
        book_id = book_response.id
        print(f"Book created: ID = {book_id}, message: {book_response.message}")

        # Borrow book
        borrow_request = library_pb2.BorrowRequest(member_id=member_id, book_id=book_id)
        borrow_response = await stub.BorrowBook(borrow_request)
        print(f"Borrow attempt: {borrow_response.message}")

        # Attempt to borrow again (should fail)
        try:
            borrow_fail_response = await stub.BorrowBook(borrow_request)
            print(f"Unexpected borrow: {borrow_fail_response.message}")
        except grpc.aio.AioRpcError as e:
            print(f"Expected failure on second borrow: {e.details()}")

        # Return book
        try:
            return_response = await stub.ReturnBook(borrow_request)
            print(f"Return book: {return_response.message}")
        except grpc.aio.AioRpcError as e:
            print(f"Error returning book: {e.details()}")


if __name__ == "__main__":
    asyncio.run(main())
