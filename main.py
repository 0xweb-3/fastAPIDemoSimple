from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}


@app.get("/users/{user_id}")
def read_user(user_id: int, skip: int = 0, limit: int = 100):
    return {"user_id": user_id, "skip": skip, "limit": limit}

from pydantic import BaseModel
class Item(BaseModel):
    name: str
    description: str = None
    price: float

@app.post("/User")
def create_user(item: Item):
    item_dict = item.model_dump()
    if item.price > 100.0:
        item_dict["price"] = item.price * 0.9
    return item_dict


