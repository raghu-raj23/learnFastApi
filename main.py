from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: Optional[float] | None = None


@app.get("/items")
def read_items():
    return [{"name": "Item Foo"}, {"name": "Item Bar"}]

if __name__ == "__main__":
    print("hello")