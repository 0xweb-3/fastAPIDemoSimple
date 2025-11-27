from typing import Optional, List

from fastapi import FastAPI, HTTPException

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


@app.get("/async_user/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

from fastapi import status

@app.get("/code/{id}", status_code=status.HTTP_201_CREATED)
def create_specific_item(id: int):
    return {"id": id}


# 数据模型
class Product(BaseModel):
    id: Optional[int] = None  # 可选，创建时自动生成
    name: str
    price: float
    stock: int = 0  # 默认库存为0


# 模拟数据库（列表）
products = [
    Product(id=1, name="笔记本电脑", price=4999.99, stock=10),
    Product(id=2, name="无线鼠标", price=99.9, stock=50)
]

# 1. 获取所有商品
@app.get("/products/", response_model=List[Product])
def get_products():
    return products

# 2. 获取单个商品
@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    # 查找商品
    product = next((p for p in products if p.id == product_id), None)
    if not product:
        # 抛出404错误
        raise HTTPException(status_code=404, detail="商品不存在")
    return product

# 3. 创建商品
@app.post("/products/", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_product(product: Product):
    # 生成新ID
    product.id = max(p.id for p in products) + 1 if products else 1
    products.append(product)
    return product

# 4. 更新商品
@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, updated_product: Product):
    product = next((p for p in products if p.id == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")
    # 更新属性
    product.name = updated_product.name
    product.price = updated_product.price
    product.stock = updated_product.stock
    return product

# 5. 删除商品
@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int):
    global products
    product = next((p for p in products if p.id == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")
    # 删除商品
    products = [p for p in products if p.id != product_id]
    return  # 204状态码不需要返回内容