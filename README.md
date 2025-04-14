# Neighborhood Library Service

This project is a simple microservice architecture for managing a digital library system. It uses **gRPC** for communication, **PostgreSQL** for persistence, and **Tortoise ORM** for database operations.

Although gRPC is the main communication protocol used, **FastAPI** is included in the project structure for future REST API extensions and possible admin interfaces or monitoring tools.

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
make dev
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
make test
```

You should see output for each step of the flow.

### 4. Inspecting the Database (PostgreSQL)

To verify the data directly in the database:

4.1. Open a shell into the PostgreSQL container:

```
make database

```

### Notes

- The client test script uses dynamically generated data for member and book creation.

- All gRPC definitions live under the proto directory.

- Tortoise ORM is used for async database access.
