# Neighborhood Library Service

A full-stack gRPC-based service for managing library members, books, and borrowing logic.

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/angatupyry/neighborhood-library-service.git
cd neighborhood-library-service
```

### 2. Starting the Application

Make sure you have Docker and Docker Compose installed.

To start all services (gRPC server, client, PostgreSQL database, etc.):

```
docker compose up --build
```

This will:

- Build all containers

- Start the gRPC server

- Start the PostgreSQL database

- Prepare the client container (used for manual test execution)

### 3. Running the Full Client Test

The client test script:

- Creates a member

- Creates a book

- Borrows the book

- Attempts a second borrow (expected to fail)

To run the test manually:

```
docker compose exec client poetry run python client/entire_flow.py
```

You should see output for each step of the flow.

### 4. Inspecting the Database (PostgreSQL)

To verify the data directly in the database:

4.1. Open a shell into the PostgreSQL container:

```
docker compose exec db psql -U postgres -d library_db

```

4.2. Run SQL queries:

```sql

SELECT * FROM member;


SELECT * FROM book;


SELECT * FROM borrow;

```

### Notes

- The client test script uses dynamically generated data for member and book creation.

- All gRPC definitions live under the proto directory.

- Tortoise ORM is used for async database access.
