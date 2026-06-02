from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello World"}



@app.get("/test")
def test():
    return {"message": "Test"}


@app.get("/test/{name}")
def test_name(name: str, number: Optional[int] = None):
    if number:
        return {"message": f"Hello {name}, this is test function number {number}..."}
    else:
        return {"message": f"Hello {name}, this is test function..."}



class Human(BaseModel):
    name: str
    age: int
    city: str


@app.post("/human_test")
def test(human: Human):
    return {
        "name": human.name,
        "age": human.age,
        "city": human.city
    }