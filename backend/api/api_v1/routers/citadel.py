from fastapi import APIRouter

router = APIRouter()

@router.get("/hello")
def hello_cit():
    return {"message": "This is Citadel!!!!!"}