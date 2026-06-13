import requests
import logging

logger = logging.getLogger(__name__)

def geocode_address(address: str):
    """
    Convert a free-text address to latitude, longitude, city, state, zip code.
    Uses Nominatim (OpenStreetMap) – free, no API key required.
    Returns a dict or None if failed.
    """
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": address,
        "format": "json",
        "limit": 1,
        "addressdetails": 1
    }
    headers = {"User-Agent": "PrimeRealtyApp/1.0"}
    try:
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data:
            result = data[0]
            lat = float(result["lat"])
            lon = float(result["lon"])
            addr_details = result.get("address", {})
            city = addr_details.get("city") or addr_details.get("town") or addr_details.get("village") or ""
            state = addr_details.get("state") or ""
            zip_code = addr_details.get("postcode") or ""
            return {
                "lat": lat,
                "lng": lon,
                "city": city,
                "state": state,
                "zip_code": zip_code
            }
    except Exception as e:
        logger.error(f"Geocoding failed for address '{address}': {e}")
    return None