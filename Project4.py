import pandas as pd
import numpy as np
import streamlit as st

drivers = pd.read_csv("drivers.csv")
lap_times = pd.read_csv("lap_times.csv")
circuits = pd.read_csv("circuits.csv")
pit_stops = pd.read_csv("pit_stops.csv")
results = pd.read_csv("results.csv")
driver_standings = pd.read_csv("driver_standings.csv")
races = pd.read_csv("races.csv")
qualifying = pd.read_csv("qualifying.csv")

