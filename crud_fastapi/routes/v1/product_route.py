from typing import List
from fastapi import APIRouter, status, Query
from crud_fastapi.models import Product, ProductUpdate, ProductView
from crud_fastapi.service.product_service import ProductService

route = APIRouter(prefix="/api/v1/product", tags=["Product"])

product_service = ProductService()


@route.get(
    "/",
    response_model=List[ProductView],
    status_code=status.HTTP_200_OK,
)
def get_all_products(
    offset: int = Query(0, description="Offset for pagination"),
    limit: int = Query(10, description="Limit for pagination"),
):
    return product_service.get_all_products(offset, limit)


@route.get("/{id}", response_model=ProductView, status_code=status.HTTP_200_OK)
def get_product_by_id(id: int):
    return product_service.get_product_by_id(id)


@route.post("/", response_model=ProductView, status_code=status.HTTP_201_CREATED)
def create_new_product(product: Product):
    return product_service.create_new_product(product)


@route.patch("/{id}", response_model=ProductView, status_code=status.HTTP_202_ACCEPTED)
def update_product_by_id(id: int, product_update: ProductUpdate):
    return product_service.update_product_by_id(id, product_update)


@route.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product_by_id(id: int):
    product_service.delete_product_by_id(id)
