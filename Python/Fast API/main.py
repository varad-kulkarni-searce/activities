from fastapi import FastAPI, HTTPException
import uvicorn
from enum import Enum

app = FastAPI()  # Creating FastAPI instance


# Basic code to check working of FastAPI.

@app.get("/")
async def root():
    return {"message": "Hello World"}

# -----------------------------------------

# Path Parameters

@app.get("/items/{item_id}")
def read_item(item_id):
    return {"item_id": item_id}

# -------------------------------------------

# Path Parameter with type:
@app.get("/items/{item_id}")
def read_item_with_type(item_id: int):
    return {"item_id": item_id}


# output if item_id type is not int: {"detail":[{"loc":["path","item_id"],"msg":"value is not a valid integer",
# "type":"type_error.integer"}]}

# -------------------------------------------------

# with Enum: Predefining possible path parameters

class CarName(str, Enum):
    bmw = "BMW"
    suzuki = "Suzuki"
    audi = "Audi"


@app.get("/cars/{car_name}")
async def get_model(car_name: CarName):
    if car_name == CarName.bmw:
        return {"car_name": car_name, "message": "This car is BMW"}

    if car_name.value == CarName.suzuki:
        return {"car_name": car_name, "message": "This car is Maruti Suzuki"}

    return {"car_name": car_name, "message": "This car is Audi"}


# ------------------------------------------------

# Handling Errors


mobiles = {"ASUS": "ASUS Zenfone Max Pro M1"}


@app.get("/mobiles/{mobile_id}")
async def read_item(mobile_id: str):
    if mobile_id not in mobiles:
        raise HTTPException(status_code=404, detail="Mobile not found")
    return {"mobiles": mobiles[mobile_id]}

if __name__ == "__main__":
    uvicorn.run("main:app")


