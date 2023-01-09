import pandas as pd 
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Literal
import numpy as np
import joblib



description = """
Welcome in my API Documentation.
This app was realized for the Getaround Project.

## Machine Learning Model's prediction:
The prediction endpoint is : 
#### '/predict'

This endpoint accepts POST Methods with JSON input data.

Below, you can copy/paste an example in python to try from your notebook:\n

If you prefer a Curl example, you'll see it in the 'Try it out' function.
```

import requests\n
import json\n
response = requests.post("http://127.0.0.1:8000/predict", json={\n
    'model_key': "Citroën", \n
    'mileage' : '200000', \n
    'engine_power':'100', \n
    'fuel': 'diesel',\n
    'paint_color' :  'black', \n
    'car_type' : 'convertible', \n
    'private_parking_available' : False, \n
    'has_gps' : False,\n
    'has_air_conditioning' : False,\n
    'automatic_car' : False,\n
    'has_getaround_connect' : True,\n
    'has_speed_regulator' : True,\n
    'winter_tires' : True\n
})\n
print(response.json())
```

"""

tags_metadata = [
    
    {
        "name": "Machine_Learning 'Prediction Endpoint'.",
        #"description": "Prediction Endpoint."
    }
]


app = FastAPI(
    title="GetAround Project API",
    description=description,
    version="0.1",
    openapi_tags=tags_metadata
)



class FormFeatures(BaseModel):
    model_key: Literal['Citroën',
 'Peugeot',
 'PGO',
 'Renault',
 'Audi',
 'BMW',
 'Ford',
 'Mercedes',
 'Opel',
 'Porsche',
 'Volkswagen',
 'KIA Motors',
 'Alfa Romeo',
 'Ferrari',
 'Fiat',
 'Lamborghini',
 'Maserati',
 'Lexus',
 'Mitsubishi',
 'Nissan',
 'SEAT',
 'Subaru',
 'Suzuki',
 'Toyota'] = Field(example='Citroën')
    mileage: int = Field(example=100000)
    engine_power: int = Field(example=100)
    fuel: Literal['diesel', 'petrol', 'hybrid_petrol', 'electro'] = Field(example='diesel')
    paint_color: Literal['black',
 'grey',
 'white',
 'red',
 'silver',
 'blue',
 'orange',
 'beige',
 'brown',
 'green'] = Field(example='black')
    car_type: Literal['convertible',
 'coupe',
 'estate',
 'hatchback',
 'sedan',
 'subcompact',
 'suv',
 'van'] = Field(example='convertible')
    private_parking_available: Literal[True, False] = Field(example=True)
    has_gps: Literal[True, False] = Field(example=True)
    has_air_conditioning: Literal[True, False] = Field(example=True)
    automatic_car: Literal[True, False] = Field(example=True)
    has_getaround_connect: Literal[True, False] = Field(example=True)
    has_speed_regulator: Literal[True, False] = Field(example=True)
    winter_tires: Literal[True, False] = Field(example=True)


@app.post("/predict")
async def to_predict(formFeatures: FormFeatures):

    # Read Data Input
    model_key_input = formFeatures.model_key
    mileage_input = formFeatures.mileage
    engine_power_input = formFeatures.engine_power
    fuel_input = formFeatures.fuel
    paint_color_input = formFeatures.paint_color
    car_type = formFeatures.car_type
    private_parking_available_input = formFeatures.private_parking_available
    has_gps_input = formFeatures.has_gps
    has_air_conditioning_input = formFeatures.has_air_conditioning
    automatic_car_input = formFeatures.automatic_car
    has_getaround_connect_input = formFeatures.has_getaround_connect
    has_speed_regulator_input = formFeatures.has_speed_regulator
    winter_tires_input = formFeatures.winter_tires


    features_list = ['model_key', 'mileage', 'engine_power', 'fuel',
       'paint_color', 'car_type', 'private_parking_available', 'has_gps',
       'has_air_conditioning', 'automatic_car', 'has_getaround_connect',
       'has_speed_regulator', 'winter_tires']
    


    # Values input to obtain prediction
    X_to_predict = pd.DataFrame([[model_key_input, mileage_input, engine_power_input, 
                        fuel_input, paint_color_input, car_type, private_parking_available_input, 
                        has_gps_input, has_air_conditioning_input, automatic_car_input,
                        has_getaround_connect_input, has_speed_regulator_input, winter_tires_input]], columns = features_list)


    # Load model
    loaded_model = joblib.load('20230108-153507-xgbregressor.joblib')

    #prediction 
    prediction = loaded_model.predict(X_to_predict)

    #format response
    prediction = prediction.tolist()[0]
    prediction = round(prediction, 2)
    response = {'prediction': prediction}

    return response




@app.get("/")
async def index():

    message = "Welcome in my app (API) realized for the Getaround Project, you'll find the prediction endpoint : '/predict' . For more informations, take a look at /docs"
    
    return message

##### if we run this file, run the code #######

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000)