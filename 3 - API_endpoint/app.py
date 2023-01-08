import pandas as pd 
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Literal
import numpy as np
import joblib



description = """
Welcome in my app realized for the Getaround Project !

## Machine Learning
You'll find the prediction endpoint : 'THISURL/predict'

This endpoint accepts POST Methods with JSON input data.
Take a look at my documentation at : 'THISURL/docs'

"""

tags_metadata = [
    
    {
        "name": "Machine_Learning",
        "description": "Prediction Endpoint."
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
 'Toyota'] = 'Citroën'
    mileage: int = 100000
    engine_power: int = 100
    fuel: Literal['diesel', 'petrol', 'hybrid_petrol', 'electro'] = 'diesel'
    paint_color: Literal['black',
 'grey',
 'white',
 'red',
 'silver',
 'blue',
 'orange',
 'beige',
 'brown',
 'green'] = 'black'
    car_type: Literal['convertible',
 'coupe',
 'estate',
 'hatchback',
 'sedan',
 'subcompact',
 'suv',
 'van'] = 'convertible'
    private_parking_available: Literal[True, False] = True
    has_gps: Literal[True, False] = True
    has_air_conditioning: Literal[True, False] = True
    automatic_car: Literal[True, False] = True
    has_getaround_connect: Literal[True, False] = True
    has_speed_regulator: Literal[True, False] = True
    winter_tires: Literal[True, False] = True



@app.get("/")
async def index():

    message = "Hello world! If you want to know how to use the API, check out documentation at `/docs`"

    return message


@app.post("/predict", tags=["Machine_Learning"])
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
    
    features_values = [ model_key_input, mileage_input, engine_power_input, 
                        fuel_input, paint_color_input, car_type, private_parking_available_input, 
                        has_gps_input, has_air_conditioning_input, automatic_car_input,
                        has_getaround_connect_input, has_speed_regulator_input, winter_tires_input,
                        ]
    # print(features_values)
    # print(np.array([features_values]))

    # Values input to obtain prediction
    X_to_predict = pd.DataFrame(np.array([features_values]), columns = features_list)
    print(X_to_predict.columns)
    print(X_to_predict.values)
    print("step1")
    # Load model
    loaded_model = joblib.load('20230108-153507-xgbregressor.joblib')
    print("step2")

    #prediction 
    prediction = loaded_model.predict(X_to_predict)
    print("step3")

    #format response
    response = {'prediction': prediction.tolist()[0]}

    return response



##### if we run this file, run the code #######

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000)