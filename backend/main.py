import boto3
import os
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from mangum import Mangum
from fastapi.responses import JSONResponse
from typing import List, Optional
from pydantic import BaseModel

from datetime import datetime, timezone

from api.api_v1 import api  

class Citadel(BaseModel):
    PK: str
    SK: str
    date : str
    name : str
    system: str
    submitter : str
    fitting : List[str]

app = FastAPI(title="Citadel App")
app.include_router(api.router)

dynamodb_client = boto3.resource('dynamodb')


TABLE_NAME = os.environ['CITADEL_TABLE']
CITADEL_TABLE = dynamodb_client.Table(TABLE_NAME) #ideally get the table name the right way

#CITADEL_TABLE = os.environ['CITADEL_TABLE']

@app.get("/hello")
def hello_world():
    return {"message": "Hello World"}

@app.post("/testcreate")
def test_create(testCreate: Citadel):
    return testCreate

@app.post("/testcreatejson")
def test_create(testCreate: Citadel):
    return testCreate.json()

#turning into a basic input test
@app.post("/citadel") 
def create_user(newPK: Citadel):

    if not newPK:
        return JSONResponse(status_code=404, content={"message": "Not Recieved Correctly"})

    newPK.date = (datetime.now(timezone.utc).isoformat()) #ideally gets the current time in UTC converted to ISO format here
    #send something in the date value json and it will get set here, can easily change this to accepting the frontend if I want or need to later by commenting above line

    CITADEL_TABLE.put_item(Item=newPK.dict()) #Pydantic cast as dict 
    
    
    return newPK 

@app.get("/users/{user_id}")
def get_user(user_id):

    result = CITADEL_TABLE.get_item(Key={'PK': user_id, 'SK': '523'}) #listed as a string in yml, doing a string here?
    item = result.get('Item')
    if not item:
        return JSONResponse(status_code=404, content={"message": "Item Not Found"})
    return jsonable_encoder(item)#blah learn how to use boto3 and then json encode the response back


handler = Mangum(app)
