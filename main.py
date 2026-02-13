from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, validate_call, ValidationError, StringConstraints, Field
from typing import Annotated

app = FastAPI()

class Item(BaseModel):
    name: str = Field(..., min_length=4)
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

# @validate_call
# def validate_name(name: Annotated[str, StringConstraints(min_length=4)]):
#     return name

try:
    name = Item(name='oytrdes', price=100)
    product_without_price = name.model_dump(exclude={'price'})
    print(product_without_price, name.model_dump(include={'name'}))
    # name = validate_name(name='raghu')
    print("Name Valid")
except ValidationError as error:
    print(f'name is not valid {error}')


@app.post("/item")
async def create_item(Item: Item):

    return Item
