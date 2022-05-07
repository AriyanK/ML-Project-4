# Formula 1 Race Predictor

For this project we selected option #2 which involved creating a publicly-available online machine learning resource.  
Our app is currently available as a Streamlit app deployed on Heroku. It can be found [here](https://project-formula1-predictions.herokuapp.com/).

## Implementation
The app allows the user to enter the name of a track from the Formula-1 World Championship. The app will then predict the placements of currently active F1 drivers using historical data on that circuit. The dataset we chose includes a wide variety of recordings of all kinds of metrics including lap times, pit stop times, race results, qualifying results, individual driver results, and circuit information. It contains data ranging from the very first season of Formula 1 in 1950 to 2022 and includes data from every F1 race.  

The dataset can be found [here](https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020?select=circuits.csv).  

We isolated the 19 currently active F1 drivers (excluding Zhou Guanyu, who doesn't have a history on most circuits due to being a new driver) and compiled data from the various CSV files for their results on every F1 circuit. Our model predicts the "position order" attribute, which gives a driver's placement in a specific race.   

The predictor variables we chose were:  

- **Lap Time**: Time in milliseconds that it took a specific driver to complete a lap in a specific race
- **Qualifying Pos**: The position that a specific driver finished in the qualifying stage before a specific race
- **Pitstop Time**: Time in milliseconds of a specific pit stop in a specific race

The app averages all the values of these 3 predictor variables and uses these aggregates as training data for the model. The data it uses are determined by the track name entered by the user; only the lap times, qualifying positions, and pitstop times of races held on that track are supplied to the model.  

The model we selected for this implementation was the sklearn Random Forest Regressor. We chose this after attempting linear regression, K-neighbors classifier, and SGD classifier which all seemed to be overfitting the data. The random forest regressor helped control overfitting and gave us values we felt were acceptable.  

We mapped the results of the model to a dictionary of individual driver ids of the 19 active drivers we were interested in, and sorted them according to the predicted "Position order" value for each to arrive at a final standing for all racers. Those who have no data on the circuit entered by the user are placed at the bottom and marked as such.  

## What we learned
This was by far the largest dataset we have worked with. It includes a lot of historical data from 1950 in several separate files. This made it difficult to isolate the variables we were interested in and taught us a lot about data wrangling and cleaning data in general. We also learned how to organize the predicted results in the specific manner we wanted for our app. We also learned how to run a ML model based on user input, which is something neither of us had done before.
