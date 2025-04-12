from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "book" (
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ,
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(255) NOT NULL,
    "author" VARCHAR(255) NOT NULL,
    "isbn" VARCHAR(13) NOT NULL UNIQUE,
    "available" BOOL NOT NULL DEFAULT True
);
        CREATE TABLE IF NOT EXISTS "borrow" (
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ,
    "id" SERIAL NOT NULL PRIMARY KEY,
    "borrow_date" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "return_date" TIMESTAMPTZ,
    "book_id" INT NOT NULL REFERENCES "book" ("id") ON DELETE CASCADE,
    "member_id" INT NOT NULL REFERENCES "member" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "book";
        DROP TABLE IF EXISTS "borrow";"""
