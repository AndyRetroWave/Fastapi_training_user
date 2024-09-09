from fastapi import FastAPI
from app.user.router import router as router_user

app = FastAPI()

app.include_router(router_user)


@app.get("/")
def read_root():
    return {"Hello": "World"}
