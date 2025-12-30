# NS OLED Departure Board

A real-time train departure display for Dutch Railways (NS) stations using a Raspberry Pi and I2C OLED display. 

In my case, I used a 0.96 inch OLED I2C display and a Raspberry Pi Zero 2W.

## Wiring
Connect the OLED display to your Raspberry Pi:

| OLED Pin | Raspberry Pi Pin | Description |
|----------|------------------|-------------|
| VCC      | Pin 1 (3.3V)     | Power |
| GND      | Pin 6 (GND)      | Ground |
| SDA      | Pin 3 (GPIO 2)   | I2C Data |
| SCL      | Pin 5 (GPIO 3)   | I2C Clock |

## Raspberry Pi Setup
### 1. Enable I2C interface on Raspberry Pi
```bash
sudo raspi-config
```
Navigate to: **Interface Options** → **I2C** → **Enable**
Reboot your Raspberry Pi:
```bash
sudo reboot
```

### 2. Install Libraries
```bash
sudo apt-get update
sudo apt-get install python3-pip
pip3 install luma.oled requests Pillow
```

### 3. Get Your NS API Key
You can get an NS API key from the [NS API Portal](https://apiportal.ns.nl). Here, I am using the reisinformatie API.
You can fetch different stations via their station codes which you can find [here](https://www.ns.nl/stations).

### 5. Run the script
You can run the script directly using python3 on the Raspberry Pi. You must also replace the `API_KEY` and `STATION_CODE`.

## Troubleshooting

You may need to change the address of your I2C display. You can check your address using:
```bash
sudo i2cdetect -y 1
```

## Automatically run it on startup
```bash
sudo nano /etc/rc.local
```
Add this line before `exit 0`:
```bash
python3 /home/pi/ns_display.py &
```
