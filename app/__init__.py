__version__ = "0.1.0"

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from app.database import TORTOISE_ORM

app = FastAPI(title="Library Service")

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=False,
    add_exception_handlers=True,
)