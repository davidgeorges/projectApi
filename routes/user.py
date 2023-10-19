from fastapi import *
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from config.Database import cursor,conn
from datetime import datetime
from schemas.user import User as UserSchema
user = APIRouter()

@user.post("/new",response_model=UserSchema)
async def create_user(user_receive : UserSchema = Body(...)):
    user = jsonable_encoder(user_receive)
    try :
        cursor.execute(f"INSERT INTO utilisateurs (Nom, Prenom, Email, DateInscription)"
                       +f"VALUES('{user["nom"]}','{user["prenom"]}','{user["email"]}','{datetime.now().strftime("%Y-%m-%d")}');")
        conn.commit()
        return JSONResponse(content="User registred with success.",status_code=status.HTTP_201_CREATED)
    except Exception as error : 
        if error.errno == 1062:
            return JSONResponse(content="Email already used.",status_code=status.HTTP_200_OK)
        return JSONResponse(content="Internal Server Error",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@user.get("/get/{id}")
async def get_user(id):
    try :
        cursor.execute(f"SELECT * FROM utilisateurs WHERE id = {id}")
        user_fetch = cursor.fetchone()
        if user_fetch : 
            user_json = {"id": user_fetch[0], "nom": user_fetch[1], "prenom": user_fetch[2], "email": user_fetch[3], "date_inscription": user_fetch[4].strftime("%Y-%m-%d")}
            return JSONResponse(content={"payload" :user_json},status_code=status.HTTP_200_OK)
        return JSONResponse(content={"error": "User not found"},status_code=status.HTTP_404_NOT_FOUND)
    except Exception as error :
        print(error)
        return JSONResponse(content="Internal Server Error",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@user.put("/update/{id}")
async def update_user(id):
    return {"message": f"Update user : {id}"}

@user.delete("/delete/{id}")
async def delete_user(id):
    try :
        cursor.execute(f"DELETE FROM utilisateurs WHERE id = {id}")
        conn.commit()
        if cursor.rowcount > 0:
            return status.HTTP_204_NO_CONTENT
        return JSONResponse(content={"error": "User not found"},status_code=status.HTTP_404_NOT_FOUND)
    except Exception as error : 
        return JSONResponse(content="Internal Server Error",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@user.get("/get/title/by/category/{category_name}")
async def get_tilte_by_category(category_name):
    try : 
        result_list = []
        cursor.callproc("PS_GetTitreByCategorie",(category_name,))
        for result in cursor.stored_results():
            for row in result.fetchall():
                result_list.append(row[0])
        return JSONResponse(content={"resultList" : result_list},status_code=status.HTTP_201_CREATED)
    except Exception as error :
        return JSONResponse(content="Internal Server Error",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@user.get("/get/user/by/loan/")
async def GetUtilisateursEmprunts():
    try :
        resFetch = []
        result_list = []
        cursor.callproc("PS_GetUtilisateursEmprunts")
        for result in cursor.stored_results():
            for row in result.fetchall():
                result_list.append({"Nom" : row[0][0], "Prenom" : row[0][1]})
        return JSONResponse(content={"resultList" : result_list},status_code=status.HTTP_201_CREATED)
    except Exception as error :
        print(error)
        return JSONResponse(content="Internal Server Error",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@user.get("/get/late/loan/list")
async def GetUtilisateursEmprunts():
    cursor.callproc("PS_ListeEmpruntsRetard")
    resFetch = []
    resList = []
    for result in cursor.stored_results():
        resFetch.append(result.fetchall())
    for res in resFetch:
        resList.append({"ID" : res[0][0], 
                        "LivreISBN" : res[0][1],
                        "UtilisateurID" : res[0][2],
                        "DateEmprunt" : res[0][3],
                        "DateRetourPrevu" : res[0][4]
                        })

    print(cursor.stored_results())
    return resList
