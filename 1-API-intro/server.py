from fastapi import FastAPI
from fastapi.routing import APIRoute
from typing import Union

app = FastAPI()

myItemList = ["fire","water","earth","wind","light","dark"]

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/names/{item_name}")
def item_name(item_name: str, q: Union[str, None] = None):
    for i in myItemList:
        if item_name == i:
            return {"Your Item": item_name,"descrption":q}
    else:
        return {"Invalid": item_name}
    
def use_route_names_as_operation_ids(app: FastAPI) -> None:
    """
    Simplify operation IDs so that generated API clients have simpler function
    names.

    Should be called only after all routes have been added.
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name  # in this case, 'read_items'

use_route_names_as_operation_ids(app)