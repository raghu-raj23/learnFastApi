from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    tax: Optional[float] | None = None


@app.get("/items/{item_name}")
async def read_items(item_name: str, company: str|None = None):
    # Here company takes query parameter and item_name is path parameter
    return [{"Item Name": item_name, "Company": company}]

@app.get("/items")
async def all_items(skip: int = 0, limit: int=10):
    dummy_data = [{"item_name": "Item1"}, {"item_name": "Item2"}, {"item_name": "Item3"},
                  {"item_name": "Item4"}, {"item_name": "Item5"}, {"item_name": "Item6"},
                  {"item_name": "Item7"}, {"item_name": "Item8"}, {"item_name": "Item9"},
                  {"item_name": "Item10"}, {"item_name": "Item11"}, {"item_name": "Item12"}]
    return dummy_data[skip : skip + limit]