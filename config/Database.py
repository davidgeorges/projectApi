import os
from dotenv import load_dotenv
import mysql.connector
load_dotenv()

# Configuration de la connexion MySQL
config = {
    "host": os.getenv("DATABASE_HOST"),
    "user": os.getenv("DATABASE_USERNAME"),
    "password": os.getenv("DATABASE_PASSWORD"),
    "database": os.getenv("DATABASE_NAME")
}

# Création de la connexion MySQL
conn = mysql.connector.connect(**config)
cursor = conn.cursor()