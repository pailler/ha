import requests
import json

@service
def get_meteo_france(lat="48.8566", lon="2.3522"):
    """Récupère la météo via l'API de Météo-France et met à jour un capteur HA."""
    
    url = f"https://api.meteo-concept.com/api/forecast/daily?token=TON_TOKEN_API&lat={lat}&lon={lon}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if "forecast" in data:
            temp_min = data["forecast"][0]["tmin"]
            temp_max = data["forecast"][0]["tmax"]
            condition = data["forecast"][0]["weather"]

            # Mettre à jour un capteur dans HA
            hass.states.set("sensor.meteo_temperature_min", temp_min, {"unit_of_measurement": "°C"})
            hass.states.set("sensor.meteo_temperature_max", temp_max, {"unit_of_measurement": "°C"})
            hass.states.set("sensor.meteo_condition", condition)

            log.info(f"Météo mise à jour: Tmin {temp_min}°C, Tmax {temp_max}°C, Condition {condition}")

        else:
            log.error("Erreur: Données météo non disponibles.")

    except Exception as e:
        log.error(f"Erreur lors de la récupération des données Météo-France: {e}")
