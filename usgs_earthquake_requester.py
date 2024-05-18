import requests
import sys
import pandas as pd
import datetime
from airium import Airium

#Request parameteres can be edited here
format: str = "geojson"
limit: int = 20
minmagnitude: float  = 2.0
url = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format={format}&limit={limit}&minmagnitude={minmagnitude}"

#Function that sends request to API, returns a JSON or terminates script if any error is occured.
def getEarthQuakeData(requestUrl):
    try:
        data = requests.get(requestUrl)
        return data.json()
    except:
        print("An error occured during data request. Please check for errors and re-run the script!")
        sys.exit(1)

#Accepts a data parameter and extracts relevant informations, and returns them in a Pandas DataFrame
def processEarthQuakeData(data):    
    location = [x["properties"]["place"] for x in data["features"]]
    magnitudes = [x["properties"]["mag"] for x in data["features"]]
    time = [datetime.datetime.fromtimestamp(x["properties"]["time"]/1000) for x in data["features"]]
    longitude = [x["geometry"]["coordinates"][0] for x in data["features"]]
    latitude = [x["geometry"]["coordinates"][1] for x in data["features"]]
    depth = [x["geometry"]["coordinates"][2] for x in data["features"]]

    df = pd.DataFrame({
        "Location": location,
        "Magnitude": magnitudes,
        "Time (UTC)": time,
        "Longitude": longitude, 
        "Latitude": latitude,
        "Depth (km)": depth
    })

    return df

#Exports processed data to HTML using Airium library
def exportEarthQuakeDataToHTML(dataframe):
    htmlTable = dataframe.to_html()
    
    a = Airium()
    a("<!DOCTYPE html>")
    with a.html(lang="pl"):
        with a.head():
            a.meta(charset="utf-8")
            a.meta(content='width=device-width, initial-scale=1', name='viewport')
            a.title(_t="Everbridge Test Assessment")
            a.link(rel="stylesheet", href="style.css")
        with a.body():
            with a.header():
                with a.h1(id="title"):
                    a("Everbridge Test Assessment")
            
            with a.section(id="tableContainer"):
                a(htmlTable)
            with a.footer():
                with a.p(id="info"):
                    a("Created by Tamas Gyetvan @ 2024")
    html = str(a)
    with open("index.html", "wb") as f:
        f.write(bytes(html, encoding="utf8"))



exportEarthQuakeDataToHTML(processEarthQuakeData(getEarthQuakeData(url)))
print("Export complete, please check root folder for index.html file!")





