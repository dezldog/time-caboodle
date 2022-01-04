# Original code taken from a few files by:
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
# -*-
# transmogrifying added by dezldog 3JAN22

import time
import subprocess
import digitalio
import board
#from gpsdclient import GPSDClient
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display.rgb import color565
from adafruit_rgb_display import st7789

# Set GPS client host
#client = GPSDClient(host="127.0.0.1")

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=240,
    height=240,
    x_offset=0,
    y_offset=80,
)

backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 180

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
font28 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
font30 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
font34 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 34)
font48 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 48)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    if buttonA.value and buttonB.value:
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        cmd = "hostname -A"
        HOST = subprocess.check_output(cmd, shell=True).decode("utf-8")
        cmd = "hostname -I | cut -d' ' -f1"
        IP = "IP: " + subprocess.check_output(cmd, shell=True).decode("utf-8")
        cmd = "date +'%a %d %b %Y'"
        DATE = subprocess.check_output(cmd, shell=True).decode("utf-8")
        cmd = "date +%T"
        TIME = subprocess.check_output(cmd, shell=True).decode("utf-8")
        GAP = " "

        y = top
        draw.text((x,y), "Local Time", font=font28, fill="#FFFFFF")
        y += font.getsize(GAP)[1]
        draw.text((x, y), "-------------------", font=font30, fill="#FFFFFF")
        y += font.getsize(GAP)[1]
        draw.text((x,y), DATE, font=font28, fill="#FFFFFF")
        y += font.getsize(DATE)[1]
        draw.text((x,y), TIME, font=font48, fill="#FFFFFF")
        y += font.getsize(TIME)[1]
        y += font.getsize(GAP)[1]
        draw.text((x, y), "Hostname", font=font28, fill="#00FF00")
        y += font.getsize(GAP)[1]
        draw.text((x, y), "-------------------", font=font30, fill="#00FF00")
        y += font.getsize(GAP)[1]
        draw.text((x, y), HOST, font=font, fill="#00FF00")
        y += font.getsize(HOST)[1]
        draw.text((x, y), IP, font=font, fill="#00FF00")
        y += font.getsize(IP)[1]

    if buttonB.value and not buttonA.value:
        draw.rectangle((0, 0, width, height), outline=0, fill=0)

        cmd = "date -u +'%a %d %b %Y'"
        UDATE = subprocess.check_output(cmd, shell=True).decode("utf-8")
        cmd = "date -u +%T"
        UTIME = "UTC:" + subprocess.check_output(cmd, shell=True).decode("utf-8")
        cmd = "python /root/lat.py"
        LAT = "LAT: " + subprocess.check_output(cmd, shell=True).decode("utf-8")
        cmd = "python /root/lon.py"
        LON = "LON: " + subprocess.check_output(cmd, shell=True).decode("utf-8")
        cmd = "python /root/fix.py"
        FIX = "FIX: " + subprocess.check_output(cmd, shell=True).decode("utf-8")

        y= top
        draw.text((x,y), "GPS Status", font=font28, fill="#FFFFFF")
        y += font.getsize(GAP)[1]
        draw.text((x, y), "-------------------", font=font30, fill="#FFFFFF")
        y += font.getsize(GAP)[1]
        draw.text((x,y), "UTC Date/Time:", font=font, fill="#00FF00")
        y += font.getsize(GAP)[1]
        draw.text((x,y), UDATE, font=font28, fill="#0000FF")
        y += font.getsize(UDATE)[1]
        draw.text((x,y), UTIME, font=font34, fill="#0000FF")
        y += font.getsize(UTIME)[1]
        y += font.getsize(GAP)[1]
        draw.text((x,y), LAT, font=font, fill="#00FF00")
        y += font.getsize(LAT)[1]
        draw.text((x,y), LON, font=font, fill="#00FF00")
        y += font.getsize(LON)[1]
        draw.text((x,y),FIX, font=font, fill="#00FF00")
        y += font.getsize(FIX)[1]

    if buttonA.value and not buttonB.value:
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
        CPU = subprocess.check_output(cmd, shell=True).decode("utf-8")
        cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%s MB  %.2f%%\", $3,$2,$3*100/$2 }'"
        MemUsage = subprocess.check_output(cmd, shell=True).decode("utf-8")
        cmd = 'df -h | awk \'$NF=="/"{printf "Disk: %d/%d GB  %s", $3,$2,$5}\''
        Disk = subprocess.check_output(cmd, shell=True).decode("utf-8")
        cmd = "cat /sys/class/thermal/thermal_zone0/temp |  awk '{printf \"CPU Temp: %.1f C\", $(NF-0) / 1000}'"
        Temp = subprocess.check_output(cmd, shell=True).decode("utf-8")

        y = top
        draw.text((x,y), "System Status", font=font28, fill="#FFFFFF")
        y += font30.getsize(GAP)[1]
        draw.text((x, y), "-------------------", font=font30, fill="#FFFFFF")
        y += font30.getsize(GAP)[1]
        draw.text((x, y), CPU, font=font30, fill="#FFFF00")
        y += font.getsize(CPU)[1]
        y += font.getsize(GAP)[1]
        draw.text((x, y), MemUsage, font=font30, fill="#00FF00")
        y += font.getsize(MemUsage)[1]
        y += font.getsize(GAP)[1]
        draw.text((x, y), Disk, font=font30, fill="#0000FF")
        y += font.getsize(Disk)[1]
        y += font.getsize(GAP)[1]
        draw.text((x, y), Temp, font=font30, fill="#FF00FF")


    # Display image.
    disp.image(image, rotation)
    time.sleep(0.1)
