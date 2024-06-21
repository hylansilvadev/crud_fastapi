from typing import List
from fastapi import APIRouter, status, HTTPException, Query
from sqlmodel import Session, select

from crud_fastapi.core.database import engine
from crud_fastapi.models import Label, LabelDB, LabelUpdate, LabelView
from crud_fastapi.service.label_service import LabelService

route = APIRouter(prefix="/api/v1/label", tags=["Label"])
label_service = LabelService

@route.get("/", response_model=List[LabelView], status_code=status.HTTP_200_OK)
def get_all_Labels(
    offset: int = Query(0, description="Offset for pagination"),
    limit: int = Query(10, description="Limit for pagination"),
):
    label_service.get_all_labels(offset, limit)


@route.get("/{id}", response_model=LabelView, status_code=status.HTTP_200_OK)
def get_Label_by_id(id: int):
    with Session(engine) as session:
        label_db = session.get(LabelDB, id)

        if not label_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi encontrado nenhum registro",
            )

        return label_db


@route.post("/", response_model=LabelView, status_code=status.HTTP_201_CREATED)
def create_new_Label(label: Label):
    label_service.create_new_label(label)


@route.patch("/{id}", response_model=LabelView, status_code=status.HTTP_202_ACCEPTED)
def update_Label_by_id(id: int, Label_update: LabelUpdate):
    with Session(engine) as session:
        label_db = session.get(LabelDB, id)

        if not label_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi encontrado nenhum registro",
            )

        label_data = Label_update.dict(exclude_unset=True)
        label_db.update_from_dict(label_data)
        session.add(label_db)
        session.commit()
        session.refresh(label_db)

        return label_db


@route.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_Label_by_id(id: int):
    with Session(engine) as session:
        label_db = session.get(LabelDB, id)

        if not label_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi encontrado nenhum registro",
            )

        session.delete(label_db)
        session.commit()
