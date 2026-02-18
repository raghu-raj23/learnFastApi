from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, Header, Path, status
from pydantic import BaseModel, validate_call, ValidationError, StringConstraints, Field
from typing import Annotated

''' 
Data Injection => Centralizing the data retrieval logic to de-couple it from DB connections, etc.
Inject a dependency into arguments of path operation functions, and FastAPI will take care of executing the dependency and
getting the return value to pass to the path operation function.

Annotated => When used along with FastAPI, it passes a fastapi inbuilt function as the second argument to the Annotated type
It can have functions like Path Body, Query, Header...
'''

app = FastAPI()

async def get_db_session():
    print("Creating DB session")
    session = {"data": {1: {"name": "Item 1"}, 2: {"name": "Item 2"}}}
    try:
        yield session
    finally:
        print("Closing DB session")

DBSession = Annotated[dict, Depends(get_db_session)]
# This is a type alias for the DB session dependency, so whenever we want to use the DB session in our path operation functions,
# we can simply use DBSession as the type hint.

async def get_user(token: Annotated[str|None, Header()]="fake-token"):
    if token == "fake-token":
        return {"username": "john_doe"}
    return None

CurrentUser = Annotated[dict|None, Depends(get_user)]

class ItemCreate(BaseModel):
    name: str
    price: float|None = None

@app.post('/item/')
async def create_item(item: ItemCreate, db: DBSession, user: CurrentUser):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    item_id = max(db["data"].keys() or [0]) + 1
    db["data"][item_id] = item.model_dump()
    return {"id": item_id, **item.model_dump()}

@app.get('/items/{item_id}')
async def read_items(item_id: Annotated[int, Path(ge=1)], db: DBSession, user: CurrentUser):
    if item_id not in db["data"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return {"id": item_id, **db["data"][item_id]}
