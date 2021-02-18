#!/usr/bin/env python

import argparse

from PIL import Image, ImageFont, ImageDraw
from font_hanken_grotesk import HankenGroteskBold, HankenGroteskMedium
from font_intuitive import Intuitive
from inky.auto import auto
from datetime import date

try:
    inky_display = auto(ask_user=True, verbose=True)
except TypeError:
    raise TypeError("You need to update the Inky library to >= v1.1.0")

try:
    inky_display.set_border(inky_display.RED)
except NotImplementedError:
    pass

# Parameters
parser = argparse.ArgumentParser()
parser.add_argument('--rund', '-rd', type=str, required=True, help="Run Distance")
parser.add_argument('--rune', '-re', type=str, required=True, help="Run Elevation")
parser.add_argument('--runc', '-rc', type=str, required=True, help="Run Count")
parser.add_argument('--runp', '-rp', type=int, required=True, help="Run Goal Percentage")

parser.add_argument('--biked', '-bd', type=str, required=True, help="Bike Distance")
parser.add_argument('--bikee', '-be', type=str, required=True, help="Bike Elevation")
parser.add_argument('--bikec', '-bc', type=str, required=True, help="Bike Count")
parser.add_argument('--bikep', '-bp', type=int, required=True, help="Bike Goal Percentage")

parser.add_argument('--hiked', '-hd', type=str, required=True, help="Hike Distance")
parser.add_argument('--hikee', '-he', type=str, required=True, help="Hike Elevation")
parser.add_argument('--hikec', '-hc', type=str, required=True, help="Hike Count")
parser.add_argument('--hikep', '-hp', type=int, required=True, help="Hike Goal Percentage")

args, _ = parser.parse_known_args()

runD = args.rund
runE = args.rune
runC = args.runc
runP = args.runp

bikeD = args.biked
bikeE = args.bikee
bikeC = args.bikec
bikeP = args.bikep

hikeD = args.hiked
hikeE = args.hikee
hikeC = args.hikec
hikeP = args.hikep

# Create a new canvas to draw on
img = Image.new("P", inky_display.resolution)
draw = ImageDraw.Draw(img)

# Load the fonts
intuitive_font = ImageFont.truetype(Intuitive, 40)
hanken_bold_font = ImageFont.truetype(HankenGroteskBold, 36)
hanken_medium_font = ImageFont.truetype(HankenGroteskBold, 22)
ChiKareGo_font = ImageFont.truetype("font/ChiKareGo.ttf", 16)
# https://forums.pimoroni.com/t/inky-phat-add-fonts/5438/5
# http://www.pentacom.jp/pentacom/bitfontmaker2/gallery/?id=3778

# Top and bottom y-coordinates for the white strip
run_bottom = int(inky_display.height * 1/3)
ride_bottom = int(inky_display.height * 2/3) 
sidebar = 100

# Draw sidebar
for y in range(0, inky_display.height):
  for x in range(0, sidebar):
    img.putpixel((x, y), inky_display.RED)

# Draw run progress lines
for y in range(run_bottom - 2, run_bottom):
  for x in range(sidebar, inky_display.width):
    img.putpixel((x, y), inky_display.BLACK)

for y in range(run_bottom - 6, run_bottom):
  for x in range(sidebar, ((inky_display.width - sidebar) * runP/100) + sidebar):
    img.putpixel((x, y), inky_display.RED)


for y in range(ride_bottom - 2, ride_bottom):
  for x in range(sidebar, inky_display.width):
    img.putpixel((x, y), inky_display.BLACK)

for y in range(ride_bottom - 6, ride_bottom):
  for x in range(sidebar, ((inky_display.width - sidebar) * bikeP/100) + sidebar):
    img.putpixel((x, y), inky_display.RED)


for y in range(inky_display.height - 2, inky_display.height):
  for x in range(sidebar, inky_display.width):
    img.putpixel((x, y), inky_display.BLACK)

for y in range(inky_display.height - 6, inky_display.height):
  for x in range(sidebar, ((inky_display.width - sidebar) * hikeP/100) + sidebar):
    img.putpixel((x, y), inky_display.RED)

# Add SideBar Headers
W, H = hanken_bold_font.getsize("Run")
X = int((sidebar - W) / 2)
Y = int((inky_display.height - H) * 1/6) - 14
draw.text((X, Y), "Run", inky_display.WHITE, font=hanken_bold_font)

W, H = hanken_bold_font.getsize("Ride")
X = int((sidebar - W) / 2)
Y = int((inky_display.height - H) * 1/2) - 6
draw.text((X, Y), "Ride", inky_display.WHITE, font=hanken_bold_font)

W, H = hanken_bold_font.getsize("Hike")
X = int((sidebar - W) / 2)
Y = int((inky_display.height - H) * 5/6)
draw.text((X, Y), "Hike", inky_display.WHITE, font=hanken_bold_font)

# Add Date
today = date.today()

W, H = ChiKareGo_font.getsize(today.strftime("%Y"))
X = sidebar - W - 10
Y = 8
draw.text((X, Y), today.strftime("%Y"), inky_display.WHITE, font=ChiKareGo_font)

W, H = ChiKareGo_font.getsize(today.strftime("%b %d"))
X = sidebar - W - 10
Y = inky_display.height - H - 12
draw.text((X, Y), today.strftime("%b %d"), inky_display.WHITE, font=ChiKareGo_font)

# Positional Display Constants

distance_center = 160
elev_center = 265
act_center = 360

# Add Run Stats

section = (inky_display.width - (sidebar))/8

W, distH = hanken_medium_font.getsize("Distance")
X = int(distance_center - W/2)
Y = 6
draw.text((X, Y), "Distance", inky_display.BLACK, font=hanken_medium_font)

W, kmH = intuitive_font.getsize(runD)
X = int(distance_center - W/2)
Y = 6 + distH + 8
draw.text((X, Y), runD, inky_display.BLACK, font=intuitive_font)

W, H = ChiKareGo_font.getsize("km")
X = int(distance_center - W/2)
Y = 6 + distH + 8 + kmH + 4
draw.text((X, Y), "km", inky_display.BLACK, font=ChiKareGo_font)


W, elevH = hanken_medium_font.getsize("Elevation")
X = int(elev_center - W/2)
Y = 6
draw.text((X, Y), "Elevation", inky_display.BLACK, font=hanken_medium_font)

W, H = intuitive_font.getsize(runE)
X = int(elev_center - W/2)
Y = 6 + elevH + 8
draw.text((X, Y), runE, inky_display.BLACK, font=intuitive_font)

W, H = ChiKareGo_font.getsize("km")
X = int(elev_center - W/2)
Y = 6 + distH + 8 + kmH + 4
draw.text((X, Y), "km", inky_display.BLACK, font=ChiKareGo_font)

W, runsH = hanken_medium_font.getsize("Runs")
X = int(act_center - W/2)
Y = 6
draw.text((X, Y), "Runs", inky_display.BLACK, font=hanken_medium_font)

W, H = intuitive_font.getsize(runC)
X = int(act_center - W/2)
Y = 6 + runsH + 8
draw.text((X, Y), runC, inky_display.BLACK, font=intuitive_font)

# Add Ride Stats

section = (inky_display.width - (sidebar))/8

W, distH = hanken_medium_font.getsize("Distance")
X = int(distance_center - W/2)
Y = run_bottom + 6
draw.text((X, Y), "Distance", inky_display.BLACK, font=hanken_medium_font)

W, kmH = intuitive_font.getsize(bikeD)
X = int(distance_center - W/2)
Y = run_bottom + 6 + distH + 7
draw.text((X, Y), bikeD, inky_display.BLACK, font=intuitive_font)

W, H = ChiKareGo_font.getsize("km")
X = int(distance_center - W/2)
Y = run_bottom + 6 + distH + 7 + kmH + 10
draw.text((X, Y), "km", inky_display.BLACK, font=ChiKareGo_font)

W, elevH = hanken_medium_font.getsize("Elevation")
X = int(elev_center - W/2)
Y = run_bottom + 6
draw.text((X, Y), "Elevation", inky_display.BLACK, font=hanken_medium_font)

W, H = intuitive_font.getsize(bikeE)
X = int(elev_center - W/2)
Y = run_bottom + 6 + elevH + 7
draw.text((X, Y), bikeE, inky_display.BLACK, font=intuitive_font)

W, H = ChiKareGo_font.getsize("km")
X = int(elev_center - W/2)
Y = run_bottom + 6 + elevH + 7 + kmH + 10
draw.text((X, Y), "km", inky_display.BLACK, font=ChiKareGo_font)

W, runsH = hanken_medium_font.getsize("Rides")
X = int(act_center - W/2)
Y = run_bottom + 6
draw.text((X, Y), "Rides", inky_display.BLACK, font=hanken_medium_font)

W, H = intuitive_font.getsize(bikeC)
X = int(act_center - W/2)
Y = run_bottom + 6 + runsH + 7
draw.text((X, Y), bikeC, inky_display.BLACK, font=intuitive_font)

# Add Hike Stats

section = (inky_display.width - (sidebar))/8

W, distH = hanken_medium_font.getsize("Distance")
X = int(distance_center - W/2)
Y = ride_bottom + 6
draw.text((X, Y), "Distance", inky_display.BLACK, font=hanken_medium_font)

W, kmH = intuitive_font.getsize(hikeD)
X = int(distance_center - W/2)
Y = ride_bottom + 6 + distH + 6
draw.text((X, Y), hikeD, inky_display.BLACK, font=intuitive_font)

W, H = ChiKareGo_font.getsize("km")
X = int(distance_center - W/2)
Y = ride_bottom + 6 + distH + 6 + kmH + 4
draw.text((X, Y), "km", inky_display.BLACK, font=ChiKareGo_font)

W, elevH = hanken_medium_font.getsize("Elevation")
X = int(elev_center - W/2)
Y = ride_bottom + 6
draw.text((X, Y), "Elevation", inky_display.BLACK, font=hanken_medium_font)

W, kmH = intuitive_font.getsize(hikeE)
X = int(elev_center - W/2)
Y = ride_bottom + 6 + elevH + 6
draw.text((X, Y), hikeE, inky_display.BLACK, font=intuitive_font)

W, H = ChiKareGo_font.getsize("km")
X = int(elev_center - W/2)
Y = ride_bottom + 6 + elevH + 6 + kmH + 4
draw.text((X, Y), "km", inky_display.BLACK, font=ChiKareGo_font)

W, runsH = hanken_medium_font.getsize("Hikes")
X = int(act_center - W/2)
Y = ride_bottom + 6
draw.text((X, Y), "Hikes", inky_display.BLACK, font=hanken_medium_font)

W, H = intuitive_font.getsize(hikeC)
X = int(act_center - W/2)
Y = ride_bottom + 6 + runsH + 6
draw.text((X, Y), hikeC, inky_display.BLACK, font=intuitive_font)

# Display the completed name badge

inky_display.set_image(img)
inky_display.show()
