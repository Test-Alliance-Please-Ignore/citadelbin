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
import copy

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
    type : Optional[str] = None  
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

#https://stackoverflow.com/questions/6696027/how-to-split-elements-of-a-list
@app.get("/count")
def get_count():
    response = CITADEL_TABLE.get_item(Key={'PK': 'TOTAL', 'SK': 'COUNT'})
    item = response["Item"]
    #SK = item[0] #might cast this 0 index list into dict?
    
    #just make it PK: TOTAL, SK: COUNT and a number value and be done with it...? Got it working as a dict

    if not item:
        return JSONResponse(status_code=404, content={"message": "Item Not Found"})
    return jsonable_encoder(item["NumberCit"])

#on the initial creation make a METADATA SK to log important info, first time citadel submitted, name, location, OWNER?
@app.post("/citadel")
def create_citadel(newCitadel: Citadel):

    if not newCitadel:
        return JSONResponse(status_code=404, content={"message": "Not Recieved Correctly"})

    response = CITADEL_TABLE.get_item(Key={'PK': 'TOTAL', 'SK': 'COUNT'})
    item = response["Item"]
    uuidVal = item["NumberCit"]

    newCitadel.PK = "Cit#" + str(uuidVal)

    newUUID = int(uuidVal)
    newUUID +=1

    CITADEL_TABLE.update_item(
        Key={'PK': 'TOTAL',
         'SK': 'COUNT'
         },
         UpdateExpression='SET NumberCit = :val',
         ExpressionAttributeValues={
             ':val': newUUID
         }
    )
    #immediately increment uuid here?

    newCitadel.date = (datetime.now(timezone.utc).isoformat())
    

    metaTag = copy.deepcopy(newCitadel)
    metaTag.SK = "METADATA"
    metaTag.fitting = None
    metaTag.type = None

    #Have only metadata with location to clean up location gsi
    #need a citadel type added to metadata
    #owner go on update tag section to allow change in ownership?
    
    newCitadel.SK = newCitadel.date
    newCitadel.system = None

    CITADEL_TABLE.put_item(Item=metaTag.dict(exclude_none=True))
    CITADEL_TABLE.put_item(Item=newCitadel.dict(exclude_none=True))


# Does the update of a citadel fit
#Here use the SK of a DATE to enable reading the newest first
@app.put("/citadel") 
def update_citadel_fit(updateFit: Citadel):

    if not updateFit:
        return JSONResponse(status_code=404, content={"message": "Not Recieved Correctly"})

    updateFit.PK = "Cit#" + str(updateFit.PK)

    #updateFit.date = (datetime.now(timezone.utc).isoformat()) Do I want the date here even though it will be the SK too?
    updateFit.SK = (datetime.now(timezone.utc).isoformat())

    #send something in the date value json and it will get set here, can easily change this to accepting the frontend if I want or need to later by commenting above line

    CITADEL_TABLE.put_item(Item=updateFit.dict()) #Pydantic cast as dict 
    
    
    return updateFit 

#https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_Query.html
@app.get("/citadels/{citadel_id}")
def get_citadel(citadel_id):

    citadel_search = "Cit#" + str(citadel_id)

    #result = CITADEL_TABLE.get_item(Key={'PK': citadel_search, 'SK': 'METADATA'}) #listed as a string in yml, doing a string here?
    #item = response.get('Item')

    #ScanIndexForward=False returns the metadata sk instead of the newest date sk.
    #Keep a query limit 1 or try to get a getItem where not eq to METADATA?
    response = CITADEL_TABLE.query(
        KeyConditionExpression=Key('PK').eq(citadel_search),
        Limit = 2,
        ScanIndexForward = False
    )
    item = response['Items'][1]
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

#5/19 Allow Updating of a citadel on DisplayCitadel
# setup UUID CITADEL COUNT, on the get item do a check for if it exsists and if not start one at 1 and go from there
# Figure out a search method on citadel name? Or just on system name as given above and only do edits on displayCit page
# Turn the locations GSI endpoint into a basic proof of concept page

