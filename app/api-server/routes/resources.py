from fastapi import APIRouter

router = APIRouter()

@router.post("/")
def request_resources():
    pass