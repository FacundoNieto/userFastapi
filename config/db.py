from sqlalchemy import create_engine, MetaData

#Creo un objeto con las propiedades y métodos necesarios para luego hacer la conexión. 
# Primero digo qué base de datos estaré utilizando con "mysql+pymysql"
# con "://usuario:contraseña" digo cuál es el usuario de nuestra base de datos
# con @localhost indico el host
# con :3306 indico el puerto que estaré utilizando
# con /dbname indico el nombre de la base de datos que vamos usar 
engine = create_engine("mysql+pymysql://usuario:contraseña@localhost:3306/dbname") #esta variable la usamos en /model/users.py

# Me conecto a la base de datos (YA NO LO HAGO MÁS ASÍ PORQUE DEJA LA CONEXIÓN ABIERTA Y GENERA PROBLEMAS EN EL RENDIMIENTO DE LA APLICACIÓN)
#conn = engine.connect() #esto mantiene abierta la conexión a la base de datos (corregir porque no la cierra y el rendimiento puede verse afectado). También, la función devuelve un objeto de conexión (acá lo llamo "conn") que se puede utilizar para enviar comandos SQL a la base de datos y recibir resultados de consultas

#invocamos la metadata:
meta_data = MetaData() #esta variable la usamos en /model/users.py

"""
La "meta data" es un objeto que contiene toda la info de la base de datos a la que nos conectamos.
"meta_data" será un objeto con toda la info de la base de datos, y sirve para que desde este código
podamos manipular esta info (crear tablas, editar valores de tablas que ya hay en la db, y demás).
Con esto sólo manipulamos la info que tenemos acá en el código, NO LA BASE DE DATOS REAL. Pero 
luego, usando funciones de la librería sqlalchemy podemos actualizar la db real con lo almacenado
en este objeto meta_data.
"""