from fastapi import FastAPI
from routes.user import user
import config.Database
app = FastAPI()

app.include_router(user,prefix="/api/user")   
