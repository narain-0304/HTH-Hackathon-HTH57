# API Key
API_KEY = 'AIzaSyCyZxm_TFM3Z-LxcJaqES_FnkEGlFIrAOk'


import google.generativeai as ai
import requests
from bs4 import BeautifulSoup
import urllib.parse

# Configure the Gemini API
ai.configure(api_key=API_KEY)
# model = ai.GenerativeModel("gemini-pro")
model = ai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat()

def get_city_coordinates(city):
    """Fetch city latitude and longitude using Open-Meteo API (Free & No API Key)."""
    open_meteo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={urllib.parse.quote(city)}&count=1"

    try:
        response = requests.get(open_meteo_url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if "results" in data and len(data["results"]) > 0:
            return data["results"][0]["latitude"], data["results"][0]["longitude"]
        else:
            return None, None

    except requests.exceptions.RequestException:
        return None, None

def get_nearby_hospitals(city):
    """Finds hospitals near the given city using OpenStreetMap Overpass API."""
    lat, lon = get_city_coordinates(city)
    if lat is None or lon is None:
        return ["❌ Could not determine city coordinates. Try a larger city or check the spelling."]

    overpass_url = "https://overpass-api.de/api/interpreter"
    query = f"""
    [out:json];
    node["amenity"="hospital"](around:10000,{lat},{lon});
    out body;
    """
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.post(overpass_url, data={"data": query}, headers=headers, timeout=10)
        response.raise_for_status()

        hospitals = response.json().get("elements", [])[:5]  # Get top 5 hospitals
        if not hospitals:
            return ["❌ No hospitals found within 10 km. Try searching a nearby city."]

        hospital_info = []
        for i, hospital in enumerate(hospitals):
            name = hospital.get("tags", {}).get("name", f"Hospital {i+1}")
            # print("1111")
            lat, lon = hospital["lat"], hospital["lon"]
            # print("2222")
            maps_url = f"https://www.google.com/maps/search/?q={lat},{lon}"
            # print("3333")
            hospital_info.append({"name": name, "location": city, "maps_url": maps_url})
            # print("4444")

        return hospital_info

    except requests.exceptions.RequestException:
        return ["❌ Error fetching hospital data."]

def py_ai_main(confirmed_disease, severity, location):
    """Processes the disease, severity, and user location, then returns results."""
    response = chat.send_message(
        f"Provide detailed information about the skin disease name present in the title {confirmed_disease} ingnoring the title itself. Include:\n"
        "- External and internal symptoms (in bullet points)\n"
        "- Steps to take care of it\n"
    )

    # Get hospital details
    hospital_info = get_nearby_hospitals(location)
    
    print(f"**Symptoms & Care Instructions:**\n{response.text}\n")

    # Return results as a dictionary for the frontend
    return {
        "disease": confirmed_disease,
        "severity": severity,
        "location": location,
        "symptoms_care": response.text,
        "hospitals": hospital_info,
    }
