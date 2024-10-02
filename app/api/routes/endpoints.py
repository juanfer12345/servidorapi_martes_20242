from fastapi import APIRouter, HTTPException #Librería para los servicios que necesito en la base de datos (Actualizar, Guardar, etc)
from sqlalchemy.orm import Session #Comunicación con la base de datos.
from typing import List
from fastapi.params import Depends #Utilizar dependencias del api para comunicación interna.
from app.api.DTO.dtos import UsuarioDTOPeticion, UsuarioDTORespuesta
from app.api.models.tablasSQL import Usuario
from app.database.configuration import SessionLocal,engine

rutas = APIRouter()

def conectarConBD():
    try:
        basedatos = SessionLocal()
        yield basedatos #Activar la base de datos
           
    except Exception as error:
        basedatos.rollback()
        raise error
    finally:
        basedatos.close()


#CONSTRUYEBDO NUESTROS SERVICIOS

#Cada servicio (operacion o transaccion en BD) debe programarse como una funcion
@rutas.post("/usuario", response_model=Usuario, summary="Registrar un usuario en la base de datos")
def guardarUsuario(datosUsuario:UsuarioDTOPeticion, database:Session=Depends(conectarConBD)):
    try:
        usuario=Usuario(
            nombres=datosUsuario.nombres,
            fechaNacimiento=datosUsuario.fechaNacimiento,
            ubicacion=datosUsuario.ubicacion,
            metaAhorro=datosUsuario.metaAhorro
        )
        #ordenandole a la base de datos
        database.add(usuario)
        database.commit()
        database.refresh(usuario)
        return usuario
    except Exception as error:
        database.rollback()
        raise HTTPException(status_code=400, detail=f"Tenemos un problema {error}")


@rutas.get("/usuario", response_model=List[UsuarioDTORespuesta], summary="Buscar todos los usuarios en BD")
def buscarUsuarios(database:Session=Depends(conectarConBD)):
    try:
        usuarios=database.query(Usuario).all()
        return usuarios
    except Exception as error:
        database.rollback()
        raise HTTPException(status_code=400, detail=f"No se puede buscar los usuarios {error}")
