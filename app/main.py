from fastapi import FastAPI

from app.api.routers import main_router

app = FastAPI(
    docs_url="/swagger"
)

app.include_router(main_router)
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
