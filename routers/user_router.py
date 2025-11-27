from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(
    prefix="/users",
    tags=["用户管理"] # 用于swag的分组
)


class User(BaseModel):
    id: Optional[int] = None
    name: str
    email: str
    age: int = None  # 可选字段


# 模拟数据库（用户列表）
users = [
    User(id=1, name="张三", email="zhangsan@example.com", age=25),
    User(id=2, name="李四", email="lisi@example.com", age=30)
]


# 2. 定义用户模块路由（路径自动拼接前缀，实际路径为"/users/"）
@router.get("/", response_model=List[User], summary="获取所有用户")
def get_all_users():
    return users


# 路径参数：用户ID（实际路径为"/users/{user_id}"）
@router.get("/{user_id}", response_model=User, summary="获取单个用户")
def get_user(user_id: int):
    user = next((u for u in users if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user


# POST请求（实际路径为"/users/"）
@router.post("/", response_model=User, summary="创建用户")
def create_user(user: User):
    user.id = max(u.id for u in users) + 1 if users else 1
    users.append(user)
    return user
