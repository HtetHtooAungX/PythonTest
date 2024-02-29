from fastapi import FastAPI
from typing import Union
from pydantic import BaseModel

ourData = {}

class Item(BaseModel):
    name : str
    price : float
    brand_name : str
    description :str | None = None

app = FastAPI()

@app.get("/get_item/{item_name}")
def get_item(item_name: str, q: Union[str, None] = None):
    temp : dict = {}
    keylist =[]
    i = 0
    if q:
        for key,value in ourData.items():
            if value["brand_name"] == item_name and value["description"] == q:
                temp.update({i : {key : value}})
                keylist.append(key)
                i+=1
    for key,value in ourData.items():
        if value["brand_name"] == item_name and key not in keylist:
            temp.update({i : {key : value}})
            i+=1
    if len(temp) == 0:
        return {"data" : "Invalid"}
    temp.update({"Q":q})
    return temp

@app.post("/save_item/{item_id}")
def save_item(item_id: int, item: Item):
    if item_id in ourData.keys():
        return {"Invaild" : "key already exist"}
    newData = {item_id : item.dict()}
    ourData.update(newData)
    print(ourData)
    return ourData

@app.put("/update_item/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id in ourData.keys():
        newData = {item_id : item.dict()}
        ourData.update(newData)
        print(ourData)
        return ourData
    return {"Item_id": "Not Found"}


@app.delete("/delete_item/{item_id}")
def delete_item(item_id: int,item: Item):
    if len(ourData) <= 0:
       return {"data" : "Invalid"}
    deleted_item = ourData.pop(item_id, None)
    return deleted_item
