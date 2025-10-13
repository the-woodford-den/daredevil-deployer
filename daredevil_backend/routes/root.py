import logfire
from fastapi import APIRouter

api = APIRouter(prefix="/")


@api.get("/")
async def get_root():
    logfire.info("Daredevil Deployer Application")
    return {"message": "Daredevil Deployer Application"}
