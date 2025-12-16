from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import requests
import os
from dotenv import load_dotenv
from fastapi import HTTPException
load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")

app = FastAPI()

# Servir carpeta static
app.mount("/static", StaticFiles(directory="static"), name="static")
print("API_KEY:", repr(API_KEY))


@app.get("/")
def serve_home():
    return FileResponse("static/index.html")



@app.get("/weather/{city}")
def get_weather(city: str):
    url = (
        f"https://weather.visualcrossing.com/"
        f"VisualCrossingWebServices/rest/services/timeline/"
        f"{city}"
        f"?unitGroup=metric"
        f"&key={API_KEY}"
        f"&contentType=json"
        f"&lang=es"
    )

    response = requests.get(url).json()

    # DEBUG (puedes quitar luego)
    print(response)

    if "currentConditions" not in response:
        raise HTTPException(
            status_code=400,
            detail=response.get("message", "Error al obtener el clima")
        )

    return {
        "temperature": response["currentConditions"]["temp"],
        "description": response["currentConditions"]["conditions"]
    }


