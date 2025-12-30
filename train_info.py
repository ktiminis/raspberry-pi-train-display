
import time
import requests
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import ImageFont
from datetime import datetime

API_KEY = "YOUR_API_KEY"
STATION_CODE = "STATION CODE"
API_URL = f"https://gateway.apiportal.ns.nl/reisinformatie-api/api/v2/departures"
UPDATE_INTERVAL = 30

serial = i2c(port=1, address=0x3C) #I2C display address. May vary.
device = ssd1306(serial)


def get_departures():
    """Fetch departure times from NS API"""
    headers = {
        "Ocp-Apim-Subscription-Key": API_KEY
    }
    params = {
        "station": STATION_CODE,
        "maxJourneys": 10
    }

    try:
        response = requests.get(API_URL, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("payload", {}).get("departures", [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []


def format_time(iso_time):
    """Convert ISO time to HH:MM format"""
    try:
        dt = datetime.fromisoformat(iso_time.replace('Z', '+00:00'))
        return dt.strftime("%H:%M")
    except:
        return iso_time


def display_departures(departures):
    """Display departure information on OLED"""
    with canvas(device) as draw:
        if not departures:
            draw.text((0, 0), "No departures", fill="white")
            draw.text((0, 12), "available", fill="white")
            return

        track1_deps = [d for d in departures if d.get("plannedTrack") == "1"]
        track2_deps = [d for d in departures if d.get("plannedTrack") == "2"]

        draw.text((0, 0), "Station Name", fill="white")
        draw.line((0, 10, 128, 10), fill="white")

        y_pos = 14

        # Display Track 1 departures first
        for i, dep in enumerate(track1_deps[:2]):  # Show max 2 from track 1
            time_str = format_time(dep.get("plannedDateTime", ""))
            direction = dep.get("direction", "Unknown")
            track = dep.get("plannedTrack", "?")
            delay = dep.get("departureDelayMinutes", 0)

            if len(direction) > 12:
                direction = direction[:12]

            line = f"{time_str} {direction[:9]}"
            if delay > 0:
                line += f" +{delay}"

            draw.text((0, y_pos), line, fill="white")
            draw.text((110, y_pos), f"{track}", fill="white")

            y_pos += 12

        for i, dep in enumerate(track2_deps[:2]):  # Show max 2 from track 2
            if y_pos > 60:
                break

            time_str = format_time(dep.get("plannedDateTime", ""))
            direction = dep.get("direction", "Unknown")
            track = dep.get("plannedTrack", "?")
            delay = dep.get("departureDelayMinutes", 0)

            if len(direction) > 12:
                direction = direction[:12]

            line = f"{time_str} {direction[:9]}"
            if delay > 0:
                line += f" +{delay}"

            draw.text((0, y_pos), line, fill="white")
            draw.text((110, y_pos), f"{track}", fill="white")

            y_pos += 12


def main():
    """Main loop"""
    print("NS Train Departures Display Started")

    try:
        while True:
            departures = get_departures()
            display_departures(departures)

            if departures:
                print(f"\nUpdated at {datetime.now().strftime('%H:%M:%S')}")
                track1 = [d for d in departures if d.get("plannedTrack") == "1"]
                track2 = [d for d in departures if d.get("plannedTrack") == "2"]

                print("Track 1:")
                for dep in track1[:2]:
                    time_str = format_time(dep.get("plannedDateTime", ""))
                    direction = dep.get("direction", "")
                    track = dep.get("plannedTrack", "")
                    print(f"  {time_str} -> {direction} (Track {track})")

                print("Track 2:")
                for dep in track2[:2]:
                    time_str = format_time(dep.get("plannedDateTime", ""))
                    direction = dep.get("direction", "")
                    track = dep.get("plannedTrack", "")
                    print(f"  {time_str} -> {direction} (Track {track})")

            time.sleep(UPDATE_INTERVAL)

    except KeyboardInterrupt:
        device.clear()


if __name__ == "__main__":
    main()
