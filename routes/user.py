from fastapi import *

user = APIRouter()

@user.post("/new")
async def create_user():
    return {"message": "New user"}

@user.get("/get/{id}")
async def get_user(id):
    return {"message": f"Getting user : {id}"}

@user.put("/update/{id}")
async def update_user(id):
    return {"message": f"Update user : {id}"}

@user.delete("/delete/{id}")
async def delete_user(id):
    return {"message": f"Delete user : {id}"}
