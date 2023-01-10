# Bloc_5
### *Industrialisation d'un algorithme d'apprentissage automatique et automatisation des processus de décision*
## **GetAround**

- **Contact**: *Christophe DERACHE*
- **E-mail**&nbsp;&nbsp;: *christophe.derache@gmail.com*

> Video link : 👉 ********************** 👈

## Subject

>*When using Getaround, drivers book cars for a specific time period, from an hour to a few days long. They are supposed to bring back the car on time, but it happens from time to time that drivers are late for the checkout.*

>*Late returns at checkout can generate high friction for the next driver if the car was supposed to be rented again on the same day : Customer service often reports users unsatisfied because they had to wait for the car to come back from the previous rental or users that even had to cancel their rental because the car wasn’t returned on time.*

>*Our Product Manager still needs to decide:*

>- *threshold: how long should the minimum delay be?*
>- *scope: should we enable the feature for all cars?, only Connect cars?*


## 1 - Data Analysis & Web Dashboard

In this folder, you'll find :
- A notebook containing all analysis and conclusion 
- The whole code for the deployed Dashboard
- It's a Streamlit app containerized with Docker and pushed on Heroku

Dashboard URL : https://bloc-5-dashboard.herokuapp.com/


## 2 - Machine Learning

In this folder, you'll find : 
- A notebook containing all machine learning models tested for this project.
- A notebook with the last training with the best model on all data. Then, I've exported this model in joblib format to use it in production.


## 3 - API Endpoint

In this folder, you'll find the code of my deployed API app:
- This API allow everybody to request my machine learning model which predict the best price to rent a car, depending on several parameters.
- It's a FastAPI app containerized with Docker and pushed on Heroku.

API URL : https://bloc-5-api.herokuapp.com/








