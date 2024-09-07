from fastapi import APIRouter

router = APIRouter()


@router.post("/regiter")
async def register_user():
    pass
