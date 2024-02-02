import databases
import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import datetime

DATABASE_URL = "sqlite:///./test.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("surname", sqlalchemy.String),
    sqlalchemy.Column("email", sqlalchemy.String),
    sqlalchemy.Column("password", sqlalchemy.String),
)

products = sqlalchemy.Table(
    "products",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("description", sqlalchemy.String),
    sqlalchemy.Column("price", sqlalchemy.Integer),
)

orders = sqlalchemy.Table(
    "orders",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id")),
    sqlalchemy.Column("product_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("products.id")),
    sqlalchemy.Column("order_date", sqlalchemy.DateTime),
    sqlalchemy.Column("status", sqlalchemy.String),
)

engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


class UserIn(BaseModel):
    name: str
    surname: str
    email: str
    password: str


class UserOut(BaseModel):
    id: int
    name: str
    surname: str
    email: str


class ProductIn(BaseModel):
    name: str
    description: str
    price: int


class ProductOut(BaseModel):
    id: int
    name: str
    description: str
    price: int


class OrderIn(BaseModel):
    user_id: int
    product_id: int
    order_date: datetime.datetime
    status: str


class OrderOut(BaseModel):
    id: int
    user_id: int
    product_id: int
    order_date: datetime.datetime
    status: str


@app.post("/users/", response_model=UserOut)
async def create_user(user: UserIn):
    query = users.insert().values(name=user.name, surname=user.surname, email=user.email, password=user.password)
    last_record_id = await database.execute(query)
    return {**user.dict(), "id": last_record_id}


@app.get("/users/", response_model=List[UserOut])
async def read_users():
    query = users.select()
    return await database.fetch_all(query)


@app.get("/users/{user_id}", response_model=UserOut)
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)


@app.put("/users/{user_id}")
async def update_user(user_id: int, user: UserIn):
    query = users.update().where(users.c.id == user_id).values(name=user.name, surname=user.surname, email=user.email, password=user.password)
    await database.execute(query)
    return {"message": "User updated successfully"}


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {"message": "User deleted successfully"}


@app.post("/products/", response_model=ProductOut)
async def create_product(product: ProductIn):
    query = products.insert().values(name=product.name, description=product.description, price=product.price)
    last_record_id = await database.execute(query)
    return {**product.dict(), "id": last_record_id}


@app.get("/products/", response_model=List[ProductOut])
async def read_products():
    query = products.select()
    return await database.fetch_all(query)


@app.get("/products/{product_id}", response_model=ProductOut)
async def read_product(product_id: int):
    query = products.select().where(products.c.id == product_id)
    return await database.fetch_one(query)


@app.put("/products/{product_id}")
async def update_product(product_id: int, product: ProductIn):
    query = products.update().where(products.c.id == product_id).values(name=product.name, description=product.description, price=product.price)
    await database.execute(query)
    return {"message": "Product updated successfully"}


@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    query = products.delete().where(products.c.id == product_id)
    await database.execute(query)
    return {"message": "Product deleted successfully"}


@app.post("/orders/", response_model=OrderOut)
async def create_order(order: OrderIn):
    query = orders.insert().values(user_id=order.user_id, product_id=order.product_id, order_date=order.order_date,
                                   status=order.status)
    last_record_id = await database.execute(query)
    return {**order.dict(), "id": last_record_id}


@app.get("/orders/", response_model=List[OrderOut])
async def read_orders():
    query = orders.select()
    return await database.fetch_all(query)


@app.get("/orders/{order_id}", response_model=OrderOut)
async def read_order(order_id: int):
    query = orders.select().where(orders.c.id == order_id)
    return await database.fetch_one(query)


@app.put("/orders/{order_id}")
async def update_order(order_id: int, order: OrderIn):
    query = orders.update().where(orders.c.id == order_id).values(user_id=order.user_id, product_id=order.product_id, order_date=order.order_date, status=order.status)
    await database.execute(query)
    return {"message": "Order updated successfully"}


@app.delete("/orders/{order_id}")
async def delete_order(order_id: int):
    query = orders.delete().where(orders.c.id == order_id)
    await database.execute(query)
    return {"message": "Order deleted successfully"}