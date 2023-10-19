# Project API - IPSSI - 2023

# Fonctionnalités
1 - Create,get,update and delete an user.
 <br>
2 - Get the title of a book by category, by using a PROCEDURE
 <br>
3 - ?
<br>

# Installation des libraries et lancement de l'application
1 - pip install -r installed_libraries.txt
2 - uvicorn main:app --reload

# Test / Exemple of use
1 - Import apiRoutes.json in POSTMAN.
 <br>
2 - Use the route "Create user", in the body section you will have a JSON containing the user informations, change the information as you want and than click on SEND.
 <br>
3 - If the user doesn't exist in the database you will have the following message : "User registred with success." and the HTTP code : 201.
<br>
4 - If the user exist in the database you will have the following message : "Email already used." and the HTTP code : 200.
<br>
5 - If its not step 3 or 4, an INTERNAL ERROR SERVOR as occured.

# Techno :
Backend : FastApi (Python) <code><img height="40" alt="react" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/python/python.png"></code>
 <br>
Frontend : ReactJS <code><img height="35" alt="react" src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/React-icon.svg/1024px-React-icon.svg.png"></code>
