from fastapi import APIRouter, Response
from starlette.status import HTTP_201_CREATED,HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
from schema.user_schema import UserSchema, DataUser
#from config.db import conn #conexión a la base de datos
from config.db import engine
from model.users import users #tabla creada
from werkzeug.security import generate_password_hash, check_password_hash
from typing import List

user = APIRouter()

@user.get("/")
def root():
    return {"message":"Hi I am FastAPI with a router"}

@user.get("/api/user", response_model=List[UserSchema]) #con response_model=List[UserSchema] mejoro la documentación... ya de por sí retornaba un array de objetos UserSchema...
def get_users():
    with engine.connect() as conn:
        result = conn.execute(users.select()).fetchall()
        return result

@user.get("/api/user/{user_id}", response_model=UserSchema)
def get_user(user_id: str):
    with engine.connect() as conn:
        result = conn.execute(users.select().where(users.c.id == user_id)).first()
        return result


@user.post("/api/user", status_code=HTTP_201_CREATED)
def create_user(data_user: UserSchema): #recibe los datos del usuario como parámetro, estos datos provienen del cliente (frontend) y son objetos de la clase UserSchema declarada en /schema/user_schema.py
    #con el uso del entorno "with" abro la conexión, ejecuto la acción, y luego cierro la conexión
    with engine.connect() as conn:
        new_user = data_user.dict() #transforma el parámetro recibido en un diccionario (antes era un objeto de tipo UserSchema)
        #ahora encripto las passwords recibidas 
        new_user["user_passw"] = generate_password_hash(data_user.user_passw, "pbkdf2:sha256:30", 30)

        conn.execute(users.insert().values(new_user)) #hace un INSERT INTO users VALUES new_user que es un diccionario con clave y valor de las columnas de la tabla users y realizo un cambio en la base de datos real... pero hace falta el commit 
        #conn.commit() # SOLO SIRVE EN LA VERSIÓN 2.0 DE SQLALCHEMY, con esto "confirmo" la transacción de la base de datos. Cuando se realizan cambios en la base de datos, estos se almacenan en una "transacción". Para asegurar la integridad de la base de datos, las transacciones deben confirmarse o revertirse explícitamente. En este caso, conn.commit() se utiliza para confirmar la transacción
    return Response(status_code = HTTP_201_CREATED)


@user.put("/api/user/{user_id}", response_model = UserSchema)
def update_user(data_update: UserSchema, user_id: str):
    with engine.connect() as conn:
        encrypted_passw = generate_password_hash(data_update.user_passw, "pbkdf2:sha256:30", 30)
        #modifico los datos del usuario recibido en la tabla users.
        conn.execute(users.update().values(name = data_update.name, username = data_update.username, user_passw = encrypted_passw).where(users.c.id == user_id))
        #retorno los datos actualizados del usuario
        result = conn.execute(users.select().where(users.c.id == user_id)).first()
        return result

@user.delete("/api/user/{user_id}", status_code= HTTP_204_NO_CONTENT)
def delete_user(user_id: str):
    with engine.connect() as conn:
        conn.execute(users.delete().where(users.c.id == user_id))
        return Response(status_code = HTTP_204_NO_CONTENT)


@user.post("/api/user/login")
def user_login(data_user: DataUser):
    with engine.connect() as conn:
        result = conn.execute(users.select().where(users.c.username == data_user.username)).first()
        #result almacena una tupla (id,name,username,user_passw) o None cuando no se encontró el usuario
        if result != None:
            check_passw = check_password_hash(result[3], data_user.user_passw) #True o False si está bien o mal la contraseña ingresada
            
            if check_passw:
                return {
                    "status":200,
                    "message":"Access Success"
                }

        return {
            "status":HTTP_401_UNAUTHORIZED,
            "message":"Access Denied"
        }
