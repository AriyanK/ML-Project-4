import pandas as pd
import numpy as np
import streamlit as st
import sklearn as sk

drivers = pd.read_csv("drivers.csv")
lap_times = pd.read_csv("lap_times.csv")
circuits = pd.read_csv("circuits.csv")
pit_stops = pd.read_csv("pit_stops.csv")
results = pd.read_csv("results.csv")
driver_standings = pd.read_csv("driver_standings.csv")
races = pd.read_csv("races.csv")
qualifying = pd.read_csv("qualifying.csv")


drivers_list = ['hamilton', 'mick_schumacher', 'russell', 'max_verstappen', 'perez', 'leclerc', 'sainz', 'norris', 'ricciardo',
               'vettel', 'stroll', 'alonso', 'ocon', 'gasly', 'tsunoda', 'bottas', 'albon', 'latifi', 'kevin_magnussen']
drivers = drivers[(drivers['driverRef'].isin(drivers_list))]
driver_ids = drivers.driverId.unique()

drivers['fullname'] = drivers['forename']  + ' ' + drivers['surname']
driver_dictionary = dict(zip(drivers.driverId, drivers.fullname))

results = results[(results['driverId'].isin(driver_ids))]
lap_times = lap_times[(lap_times['driverId'].isin(driver_ids))]
pit_stops = pit_stops[(pit_stops['driverId'].isin(driver_ids))]
driver_standings = driver_standings[(driver_standings['driverId'].isin(driver_ids))]
qualifying = qualifying[(qualifying['driverId'].isin(driver_ids))]

merged = pd.merge(qualifying, results,  how='inner', left_on=['raceId', 'driverId'], right_on=['raceId','driverId'])
new_laps = lap_times.groupby(['raceId','driverId']).mean().reset_index()
merged = pd.merge(merged, new_laps,  how='inner', left_on=['raceId', 'driverId'], right_on=['raceId','driverId'])
new_pits = pit_stops.groupby(['raceId','driverId']).mean().reset_index()
merged = pd.merge(merged, new_pits,  how='inner', left_on=['raceId', 'driverId'], right_on=['raceId','driverId'])
merged.rename(columns = {'milliseconds_x':'race_time'}, inplace = True)
merged.rename(columns = {'milliseconds_y':'lap_time'}, inplace = True)
merged.rename(columns = {'milliseconds':'pitstop_time'}, inplace = True)
merged.rename(columns = {'position_x':'qualifying_pos'}, inplace = True)

training = merged[['pitstop_time', 'lap_time', 'positionOrder', 'fastestLapSpeed', 'qualifying_pos']].copy()
training = training.drop("fastestLapSpeed", axis=1)
training_labels = training['positionOrder']

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error


some_data1 = training[0:]
some_data1 = some_data1.drop("positionOrder", axis=1)
some_labels1 = training_labels[0:]

forest_reg = RandomForestRegressor(n_estimators=100, random_state=42)
forest_reg.fit(some_data1, some_labels1)

merged1 = merged.copy(deep=True)
merged1 = pd.merge(merged1, races,  how='inner', left_on=['raceId'], right_on=['raceId'])
merged1 = merged1.groupby(['name','driverId']).mean().reset_index()
merged1 = merged1[['driverId', 'name', 'pitstop_time', 'lap_time', 'qualifying_pos']].copy()


def getPredictions(raceName):
    data = merged1.loc[merged1['name'] == raceName]
    if(data.size == 0):
        st.write("Invalid Circuit Name")
        st.write ("Please re-enter a valid circuit name")
        return None
    data.name.unique()
    results = {}
    for i in (1, 4, 20, 842, 815, 817, 822, 825, 830, 832, 839, 840, 844,
       846, 847, 848, 849, 852, 854):
        driverData = data.loc[data['driverId'] == i]
#         print(driverData)
        if(driverData.size == 0):
            results[i] = 10000
            continue
        pitstopTime = driverData['pitstop_time'].mean()
#         print(pitstopTime)
        lapTime = driverData['lap_time'].mean()
        qualifyingPos = driverData['qualifying_pos'].mean()
        df = pd.DataFrame(columns = ['pitstop_time', 'lap_time', 'qualifying_pos'])
#         df['pitStopTime'] = 1000
        df.loc[len(df.index)] = [pitstopTime, lapTime, qualifyingPos]
        
        final_predictions = forest_reg.predict(df)
        results[i] = final_predictions[0]
#         for i in ('apple', 'banana', 'carrot'):
#             fruitdict[i] = locals()[i]
    results['Guan'] = 20000
    results = sorted(results.items(), key=lambda x: x[1], reverse=False)
    placement = 1
    for i in results:
        if(i[1] == 10000):
            st.write(placement, ' ', driver_dictionary[i[0]], ' (Placed low due to lack of data)')
            placement += 1
        elif (i[1]==20000):
            st.write(placement, ' ', 'Zhou Guanyu', ' (Placed low due to lack of data)')
        else:
            st.write(placement, ' ', driver_dictionary[i[0]])
            placement += 1
    return results

st.title("Formula 1 Race Predictor")
st.write("Upcoming Cicuits: ", " Spanish Grand Prix, Monaco Grand Prix, Azerbaijan Grand Prix, Canadian Grand Prix, British Grand Prix, Austrian Grand Prix, French Grand Prix, Hungarian Grand Prix")
with st.form("my_form"):
    text = st.text_input("Enter Circuit Name")
    
    
    
# Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write("Prediction for Final Standings")
        x = text
        final_results = getPredictions(x)
        
        