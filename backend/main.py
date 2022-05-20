import boto3
from boto3.dynamodb.conditions import Key
import os
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from mangum import Mangum
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel

from datetime import datetime, timezone

from api.api_v1 import api  

# GSI .yml info https://gist.github.com/sdymj84/940a983c86e2d2aa1e92401128789bff
class Fitting(BaseModel):
    High: List[str]
    Mid: List[str]
    Low: List[str]
    Rig: List[str]
    Service: List[str] 

class Citadel(BaseModel):
    PK: str
    SK: str
    date : str
    name : str
    system: Optional[str] = None
    submitter : str
    fitting : Optional[Fitting] = None #not sure if this will make an array of lists that are optional lol

origins = [ "http://localhost:3000"]

app = FastAPI(title="Citadel App")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(api.router)

dynamodb_client = boto3.resource('dynamodb')


TABLE_NAME = os.environ['CITADEL_TABLE']
CITADEL_TABLE = dynamodb_client.Table(TABLE_NAME) #ideally get the table name the right way

#CITADEL_TABLE = os.environ['CITADEL_TABLE']

@app.get("/hello")
def hello_world():
    return {"message": "Hello World"}

#on the initial creation make a METADATA SK to log important info, first time citadel submitted, name, location, OWNER?
@app.post("/citadel")
def create_citadel(newCitadel: Citadel):

    if not newCitadel:
        return JSONResponse(status_code=404, content={"message": "Not Recieved Correctly"})
    #idea being making this part input the meta data then handing over the info to the update or something to put in the first fitting data
    newCitadel.date = (datetime.now(timezone.utc).isoformat())
    newCitadel.SK = "Metadata"

    CITADEL_TABLE.put_item(Item=newCitadel.dict())


# Does the update of a citadel fit
#Here use the SK of a DATE to enable reading the newest first
@app.put("/citadel") 
def update_citFit(updateFit: Citadel):

    if not updateFit:
        return JSONResponse(status_code=404, content={"message": "Not Recieved Correctly"})

    updateFit.date = (datetime.now(timezone.utc).isoformat()) #ideally gets the current time in UTC converted to ISO format here
    #send something in the date value json and it will get set here, can easily change this to accepting the frontend if I want or need to later by commenting above line

    CITADEL_TABLE.put_item(Item=updateFit.dict()) #Pydantic cast as dict 
    
    
    return updateFit 

@app.get("/users/{user_id}")
def get_user(user_id):

    result = CITADEL_TABLE.get_item(Key={'PK': user_id, 'SK': '523'}) #listed as a string in yml, doing a string here?
    item = result.get('Item')
    if not item:
        return JSONResponse(status_code=404, content={"message": "Item Not Found"})
    return jsonable_encoder(item)#blah learn how to use boto3 and then json encode the response back


#https://stackoverflow.com/questions/35758924/how-do-we-query-on-a-secondary-index-of-dynamodb-using-boto3
@app.get("/locations/{system}")
def get_location(system):

    response = CITADEL_TABLE.query(IndexName="CitadelPerSystem",
    KeyConditionExpression=Key('system').eq(system)
    )

    item = response['Items']

    if not item:
        return JSONResponse(status_code=404, content={"message": "Item Not Found"})
    return jsonable_encoder(item)



handler = Mangum(app)
