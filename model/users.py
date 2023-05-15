from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
#importamos el motor de conexión (que no es la conexión -que es "conn"-) y la metadata (la info que hay en la db)
from config.db import engine, meta_data

#creamos una estructura de una tabla llamada users que recibe la metadata de la variable importada meta_data:
#el 3er parámetro de Table() son las columnas de la tabla que estamos creando
users = Table("users", meta_data,
                Column("id", Integer, primary_key=True),
                Column("name", String(255), nullable=False),  # nullable=False hace que esta columna no puede estar vacía
                Column("username", String(255), nullable=False),
                Column("user_passw", String(255), nullable=False)
                )
#con esto se incorporó la tabla "users" al objeto "meta_data", pero todavía no se cargó en la db real

#ahora actualizamos la db real
meta_data.create_all(engine)