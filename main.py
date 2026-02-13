from typing import Optional
from fastapi import Depends, FastAPI
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

@app.get('/items')
async def read_items(q: Annotated[Optional[str], StringConstraints(min_length=3, max_length=50)] = None):
    