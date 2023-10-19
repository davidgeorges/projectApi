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
        return JSONResponse(content="Internal Server Error",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@user.put("/update/")
async def update_user(id = Query(None),nom = Query(None),prenom  = Query(None),email = Query(None) ):    
    set_clauses = []

    if nom is not None:
        set_clauses.append(f"Nom = '{nom}'")
    if prenom is not None:
        set_clauses.append(f"Prenom = '{prenom}'")
    if email is not None:
        set_clauses.append(f"Email = '{email}'")

    set_clause = ", ".join(set_clauses)
    if set_clause:
        sql_query = f"UPDATE utilisateurs SET {set_clause} WHERE id = {id};"
        try :
            cursor.execute(sql_query)
            conn.commit()
            if cursor.rowcount <= 0:
                return Response(status_code=status.HTTP_204_NO_CONTENT)
            return JSONResponse(content={"message": "User updated successfully"},status_code=status.HTTP_200_OK)
        except Exception as error :
            return JSONResponse(content="Internal Server Error",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)                  
    return JSONResponse(content={"message": "No valid data provided for update"}, status_code=status.HTTP_400_BAD_REQUEST)

@user.delete("/delete/{id}")
async def delete_user(id):
    try :
        cursor.execute(f"DELETE FROM utilisateurs WHERE id = {id}")
        conn.commit()
        if cursor.rowcount > 0:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
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
async def get_user_by_loan():
    try :
        res_fetch = []
        result_list = []
        cursor.callproc("PS_GetUtilisateursEmprunts")
        for result in cursor.stored_results():
            res_fetch.append(result.fetchall())
        for res in res_fetch[0]:
            result_list.append({"Nom" : res[0], "Prenom" : res[1]})
        return JSONResponse(content={"payload" : result_list},status_code=status.HTTP_201_CREATED)
    except Exception as error :
        return JSONResponse(content="Internal Server Error",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@user.get("/get/late/loan/list")
async def get_user_list_by_late_loan():
    try : 
        cursor.callproc("PS_ListeEmpruntsRetard")
        res_fetch = []
        result_list = []
        for result in cursor.stored_results():
            res_fetch.append(result.fetchall())
        for res in res_fetch:
            result_list.append({"ID" : res[0][0], 
                            "LivreISBN" : res[0][1],
                            "UtilisateurID" : res[0][2],
                            "DateEmprunt" : res[0][3],
                            "DateRetourPrevu" : res[0][4]
                            })
        return result_list
    except Exception as error :
        return JSONResponse(content="Internal Server Error",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
