from typing import List
from fastapi import HTTPException, status, Query
from sqlmodel import Session, select

from crud_fastapi.core.database import engine
from crud_fastapi.models.label_model import LabelDB, LabelView
from crud_fastapi.models.product_model import Product, ProductDB, ProductView


class ProductService:
    def create_new_product(self, product: Product) -> ProductDB:
        product_db = ProductDB(**product.model_dump(exclude_none=True))
        with Session(engine) as session:
            session.add(product_db)
            session.commit()
            session.refresh(product_db)

            return product_db

    def get_all_products(
        self,
        offset: int = Query(0, description="Offset for pagination"),
        limit: int = Query(10, description="Limit for pagination"),
    ) -> List[ProductDB]:
        smt = (
            select(ProductDB, LabelDB)
            .where(ProductDB.label_id == LabelDB.id)
            .offset(offset)
            .limit(limit)
        )

        with Session(engine) as session:
            products_list = session.exec(smt).all()

            result = []
            for product, label in products_list:
                result.append(
                    ProductView(
                        **product.model_dump(), label=LabelView(**label.model_dump())
                    )
                )

            return result

    def get_product_by_id(id: int) -> ProductDB:
        with Session(engine) as session:
            product_db = session.get(ProductDB, id)

            if not product_db:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Não foi encontrado nenhum registro",
                )

            return product_db

    def update_product_by_id(id: int, product_data: Product) -> ProductDB:
        with Session(engine) as session:
            product_db = session.get(ProductDB, id)

            if not product_db:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Não foi encontrado nenhum registro",
                )
            product_update = product_data.model_dump(exclude_none=True)
            product_db.sqlmodel_update(product_update)
            session.add(product_db)
            session.commit()
            session.refresh(product_db)

            return product_db

    def delete_product_by_id(id: int) -> None:
        with Session(engine) as session:
            product_db = session.get(ProductDB, id)

            if not product_db:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Não foi encontrado nenhum registro",
                )
            session.delete(product_db)
            session.commit()
