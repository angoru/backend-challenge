from fastapi import FastAPI
from tortoise import Tortoise

from app.api.api_v1.api import router as api_router
from mangum import Mangum
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World!"}


app.include_router(api_router, prefix="/api/v1")
# handler = Mangum(app)

register_tortoise(
    app,
    db_url="sqlite://app/data/data.sqlite",
    modules={"models": ["app.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
