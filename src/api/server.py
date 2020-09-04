from fastapi import FastAPI
from pydantic import BaseModel, constr
from uuid import UUID, uuid4


app = FastAPI()


class UserInput(BaseModel):
    id: int
    titulo: constr(min_length=3, max_length=50)
    descricao: constr(max_length=140)


class User_id(UserInput):
    id: UUID


arq = []


@app.get("/user")
def listar():
    return arq


@app.post("/user", response_model=User_id)
def criar(users: UserInput):
    input_new = users.dict()
    input_new.update({"id": uuid4()})
    return input_new
