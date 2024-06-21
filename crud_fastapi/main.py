from fastapi import FastAPI

from crud_fastapi.core.database import create_db_and_tables

from crud_fastapi.routes.v1.product_route import route as product_route
from crud_fastapi.routes.v1.label_route import route as label_route
from crud_fastapi.routes.v1.user_route import route as user_route


app = FastAPI()

app.include_router(product_route)
app.include_router(label_route)
app.include_router(user_route)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
