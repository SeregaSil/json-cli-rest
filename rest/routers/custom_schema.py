from fastapi import APIRouter, HTTPException, Depends
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from copy import deepcopy
from rest.database import get_session
from rest.db_model import Apps, Status
from rest.models.custom_schema import *

router = APIRouter(
    prefix = '/custom_schema',
    tags=['Custom_schema']
)

@router.post('')
def create_custom_schema(custom_schema: Custom_schema, db: Session = Depends(get_session)):
    try:
        if custom_schema.kind != 'custom_schema':
            raise HTTPException(status_code=400, detail='Неверный тип документа (kind)')

        app = Apps(
            kind=custom_schema.kind,
            name=custom_schema.name,
            version=custom_schema.version,
            description=custom_schema.description,
            state=Status.NEW,
            json=custom_schema.dict()
        )
        db.add(app)
        db.commit()
    
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
    return {'status': 'success'}


@router.get('/{uuid}')
def get_by_uuid(uuid: UUID, db: Session = Depends(get_session)):
    try:
        app = db.get(Apps, uuid)
        if not app:
            raise HTTPException(status_code=404, detail='Объект не найден')
    
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {'data': app}


@router.get('/{uuid}/state')
def get_state(uuid: UUID, db: Session = Depends(get_session)):
    try:
        app = db.get(Apps, uuid)
        if not app:
            raise HTTPException(status_code=404, detail='Объект не найден')
    
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {'state': app.state}


@router.delete('/{uuid}')
def delete_custom_schema(uuid: UUID, db: Session = Depends(get_session)):
    try:
        app = db.get(Apps, uuid)
        if not app:
            raise HTTPException(status_code=404, detail='Объект не найден')

        db.delete(app)
        db.commit()

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {'status': 'success'}


@router.put('/{uuid}/state')
def update_state(uuid: UUID, state: Status, db: Session = Depends(get_session)):
    try:
        app = db.get(Apps, uuid)
        if not app:
            raise HTTPException(status_code=404, detail='Объект не найден')

        app.state = state
        db.commit()

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return {'status': 'success'}


@router.put('/{uuid}/list_objects')
def update_list_objects(uuid: UUID, list_objects: List[List_objects], db: Session = Depends(get_session)):
    try:
        app = db.get(Apps, uuid)
        if not app:
            raise HTTPException(status_code=404, detail='Объект не найден')
        
        data = deepcopy(app.json)
        data['list_objects'] = list_objects.dict()
        app.json = data

        db.commit()

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return {'status': 'success'}

        
@router.put('/{uuid}/configuration')
def update_configuration(uuid: UUID, configuration: Configuration, db: Session = Depends(get_session)):
    try:
        app = db.get(Apps, uuid)
        if not app:
            raise HTTPException(status_code=404, detail='Объект не найден')
        
        data = deepcopy(app.json)
        data['configuration'] = configuration.dict()
        app.json = data

        db.commit()

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return {'status': 'success'}

        
@router.put('/{uuid}/configuration/specification')
def update_specification(uuid: UUID, specification: Specification, db: Session = Depends(get_session)):
    try:
        app = db.get(Apps, uuid)
        if not app:
            raise HTTPException(status_code=404, detail='Объект не найден')
        
        data = deepcopy(app.json)
        data['configuration']['specification'] = specification.dict()
        app.json = data

        db.commit()

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return {'status': 'success'}

        
@router.put('/{uuid}/configuration/settings')
def update_settings(uuid: UUID, settings: Settings, db: Session = Depends(get_session)):
    try:
        app = db.get(Apps, uuid)
        if not app:
            raise HTTPException(status_code=404, detail='Объект не найден')
        
        data = deepcopy(app.json)
        data['configuration']['settings'] = settings.dict()
        app.json = data

        db.commit()

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return {'status': 'success'}

        