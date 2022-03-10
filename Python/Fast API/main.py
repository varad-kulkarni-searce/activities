from fastapi import FastAPI, HTTPException, Depends
import uvicorn
from enum import Enum
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

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
def get_model(car_name: CarName):
    if car_name == CarName.bmw:
        return {"car_name": car_name, "message": "This car is BMW"}

    if car_name.value == CarName.suzuki:
        return {"car_name": car_name, "message": "This car is Maruti Suzuki"}

    return {"car_name": car_name, "message": "This car is Audi"}

# ------------------------------------------------

# Operations (HTTP Methods..)

list_of_username = list()

#get method (to read)
@app.get("/user/{user_name}")
async def user_details(user_name: str):
    return {"name": user_name}

#put method (to update)
@app.put("/username/{user_name}")
async def put_data(user_name: str):
    list_of_username.append(user_name)
    return {"username": user_name}

#post method (to create)
@app.post("/postData")
async def postUserData(user_name: str):
    list_of_username.append(user_name)
    return {"usernames": list_of_username}

#delete method (to delete)
@app.delete("/deleteData/{user_name}")
async def deleteUserData(user_name: str):
    list_of_username.remove(user_name)
    return {"usernames": list_of_username}

# Combining all the operations:
@app.api_route("/userOperations", methods=['GET', 'POST', 'PUT', 'DELETE'])
async def handleUserData(user_name: str):
    return {"username": user_name}

# -------------------------------------------------

# Handling Errors

mobiles = {"ASUS": "ASUS Zenfone Max Pro M1"}


@app.get("/mobiles/{mobile_id}")
async def read_item(mobile_id: str):
    if mobile_id not in mobiles:
        raise HTTPException(status_code=404, detail="Mobile not found")
    return {"mobiles": mobiles[mobile_id]}

# ------------------------------------------------------------

# Security (Authentication) in Fast API.

# creating instance of OAuthPasswordBearer class with tokenurl as parameter.
# Parameter contains the URL that the client (frontend) will use to send username and password in order to get the token.
# OAuth2PasswordBearer ensures that user is providing username and password everytime.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# To generate the token using the form data:
# Dependency injection used to make OAuth2PasswordRequestForm dependent on from_data.
@app.post("/token")
async def token_generate(form_data: OAuth2PasswordRequestForm = Depends()):
    return {'access_token': form_data.username + 'token'}


# For authentication:
@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}

# ---------------------------------------------------------------------------

# Pagination

from pydantic import BaseModel

from fastapi_pagination import Page, add_pagination, paginate

class User(BaseModel):
    name: str
    surname: str


users = [
    User(name='Varad', surname='Kulkarni'),
    User(name='Mark', surname='Talyor')
]


@app.get('/users', response_model=Page[User])
async def get_users():
    return paginate(users)


add_pagination(app)



if __name__ == "__main__":
    uvicorn.run("main:app")
