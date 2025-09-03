# app/auth.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from jose import JWTError, jwt
from datetime import datetime, timedelta
from neo4j import GraphDatabase
import uuid

router = APIRouter()

# JWT config
SECRET_KEY = "SUPER_SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Kết nối Neo4j
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "BENCHAN2025"))

# Pydantic models
class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

# Helper: tạo token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# API Register
@router.post("/register")
def register(user: RegisterRequest):
    with driver.session() as session:
        existing = session.run("MATCH (u:User {email:$email}) RETURN u", {"email": user.email}).single()
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
        uid = str(uuid.uuid4())
        session.run(
            "CREATE (u:User {id:$id, name:$name, email:$email, password:$password})",
            {"id": uid, "name": user.name, "email": user.email, "password": user.password},
        )
    return {"msg": "Register success", "user": {"id": uid, "name": user.name, "email": user.email}}

# API Login
@router.post("/login")
def login(req: LoginRequest):
    with driver.session() as session:
        user = session.run(
            "MATCH (u:User {email:$email, password:$password}) RETURN u",
            {"email": req.email, "password": req.password},
        ).single()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        u = user["u"]
        token = create_access_token({"sub": u["id"]})
        return {
            "msg": "Login success",
            "user": {"id": u["id"], "name": u["name"], "email": u["email"]},
            "access_token": token,
            "token_type": "bearer"
        }
