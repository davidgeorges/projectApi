from datetime import date
from pydantic import BaseModel,EmailStr


class User(BaseModel):
    nom : str
    prenom : str
    email : EmailStr
    dateInscription : date = None