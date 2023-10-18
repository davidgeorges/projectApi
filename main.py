from fastapi import FastAPI
from routes.user import user
from config.Database import engine
app = FastAPI()

app.include_router(user,prefix="/api/user")   
