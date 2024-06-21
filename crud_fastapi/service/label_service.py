from typing import List
from fastapi import HTTPException, Query, status
from sqlmodel import Session, select

from crud_fastapi.core.database import engine
from crud_fastapi.models.label_model import Label, LabelDB


class LabelService:
    def create_new_label(label: Label) -> LabelDB:
        label_db = LabelDB(**label.model_dump(exclude_none=True))

        with Session(engine) as session:
            try:
                session.add(label_db)
                session.commit()
                session.refresh(label_db)

                return label_db
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to create label: {e}",
                )

    def get_all_labels(
        offset: int = Query(0, description="Offset for pagination"),
        limit: int = Query(10, description="Limit for pagination"),
    ) -> List[LabelDB]:
        with Session(engine) as session:
            labels_list = session.exec(
                select(LabelDB).offset(offset).limit(limit)
            ).all()

            if not labels_list:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Não foram encontrados nenhum registro",
                )

            return labels_list
