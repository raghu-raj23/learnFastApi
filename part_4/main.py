from typing import Annotated

from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
app = FastAPI()

class Item(BaseModel):
    name: str = Field(..., min_length=4)
    description: str | None = None
    price: float

class Offer(BaseModel):
    offer: str

'''
To accept N number of parameters in the request body we use FastAPI body
We should be using the Base Model and Body in a hybrid approach so that validation and accepting of N number of 
parameters can be taken as input
'''

@app.post("/item-old")
async def create_item (name:str = Body(...), description: str = Body(None), price: float = Body(...), offer: float = Body(None)):
    item = {"name": f'{name} yess', "price": price}
    if description: item['description'] = description
    if offer: item['offer'] = offer
    return item

@app.post("/item")
async def create_items(item: Item, offer: Offer, extras: Annotated[str, Body()]):
    return {"item":item, "offer": offer, 'extras': extras}
