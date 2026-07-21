"""Day 59 — 认证 API 路由"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/api/v1/auth", tags=["认证"])

# 内存存储（教学演示，生产用数据库）
_users_db: dict[str, dict] = {}


class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/register")
def register(req: RegisterRequest) -> dict:
  if req.username in _users_db:
      raise HTTPException(400, "用户名已存在")
  from app.auth.service import hash_password
  _users_db[req.username] = {"email": req.email, "password": hash_password(req.password)}
  return {"message": "注册成功", "username": req.username}


@router.post("/login")
def login(req: LoginRequest) -> dict:
    user = _users_db.get(req.username)
    if not user:
        raise HTTPException(401, "用户不存在")
    from app.auth.service import verify_password, create_access_token
    if not verify_password(req.password, user["password"]):
        raise HTTPException(401, "密码错误")
    return {"access_token": create_access_token(1), "token_type": "bearer"}
