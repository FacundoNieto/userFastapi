from pydantic import BaseModel #con esta clase generaremos objetos con atributos de tipado fuerte y así FastAPI puede validar datos provenientes del cliente (frontend) con mayor eficiencia https://fastapi.tiangolo.com/es/python-types/
from typing import Optional

class UserSchema(BaseModel):
    id: Optional[str] #no es necesario que se le pase como parámetro el valor de id porque se declaró como opcional
    name: str
    username: str
    user_passw: str

class DataUser(BaseModel):
    username: str
    user_passw: str

"""
La clase UserSchema hereda las propiedades de la clase BaseModel.
Los objetos de clase UserSchema, como lo hace normalmente cualquier objeto, pueden crearse pasándole 
los datos como atributo al llamado de UserSchema()
Por ejemplo:

class UserSchema(BaseModel):
    id: Optional[str]
    name: str
    username: str
    user_passw: str

objetoUS = UserSchema(id = "1", name = "Nombre", username = "userName", user_passw = "12345")

y el objetoUS tendrá esos valores cargados como atributos.

Pero la gran ventaja de BaseModel es que no tenés que andar creando los métodos init, setter, getter etc
en la clase UserSchema... BaseModel configura todo
Ver minuto 1:58:20 video https://www.youtube.com/watch?v=_y9qQZXE24A

Además, cuando alguna función que se ejecuta en algún método de http (get post put delete etc) 
(y que se haga con FastAPI) retorna una lista de objetos como "objetoUS" (clase de UserSchema que hereda
de BaseModel), a esa lista la transforma en un objeto JSON antes de retornarla... lo hace automáticamente
porque detecta que esos objetos son de una clase que heredó las propiedades de BaseModel.
"""