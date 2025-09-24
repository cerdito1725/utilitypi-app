
. /home/neal/scripts/waveshare/env.sh

#function log {
#    echo "---------------------------------------"
#    echo ${1^^}
#    echo "---------------------------------------"
#}
echo "Add weather info"
python3 /home/neal/scripts/waveshare/WeatherSolar.py

echo "Export to PNG"

WAVESHARE_WIDTH=800
WAVESHARE_HEIGHT=480

/usr/bin/cairosvg -u -o /home/neal/scripts/waveshare/screen-output.png -f png --dpi 300 --output-width $WAVESHARE_WIDTH --output-height $WAVESHARE_HEIGHT /home/neal/scripts/waveshare/WeatherSolarOutput.svg

echo "Display on epaper"

python3 /home/neal/scripts/waveshare/display.py /home/neal/scripts/waveshare/screen-output.png
