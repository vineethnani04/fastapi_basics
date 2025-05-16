from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello from the root!"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello, {name}!"}

@app.get("/items")
async def read_items(category:str = "all"):
    return{category: category}

class Item(BaseModel):
    name:str
    price:float = Field(gt=0, description="Price must be greater than 0")
    quantity:int = Field(ge=1, description="Quantity must be at least 1")

@app.post("/items/")
async def create_item(item: Item):
    return{"message": f"{item.quantity} units of '{item.name}' added!", "price": item.price}

fake_items_db = {
    1: {"name": "Pen", "price": 1.5, "quantity": 10},
    2: {"name": "Notebook", "price": 3.0, "quantity": 5}
}

@app.get("/items/{item_id}")
def get_item(item_id: int):
    item = fake_items_db.get(item_id)
    if not item:
        return {"error": "Item not found"}
    return item

from fastapi.responses import JSONResponse

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    return JSONResponse(content={"message": f"Item {item_id} deleted"}, status_code=204)
