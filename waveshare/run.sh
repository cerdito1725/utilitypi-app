
#. /home/neal/scripts/waveshare/env.sh
#
#function log {
#    echo "---------------------------------------"
#    echo ${1^^}
#    echo "---------------------------------------"
#}
#echo "Add weather info"
#python3 /home/neal/scripts/waveshare/WeatherSolar.py
#
#echo "Export to PNG"
#
#WAVESHARE_WIDTH=800
#WAVESHARE_HEIGHT=480

#/usr/bin/cairosvg -u -o /home/neal/scripts/waveshare/screen-output.png -f png --dpi 300 --output-width $WAVESHARE_WIDTH --output-height $WAVESHARE_HEIGHT /home/neal/scripts/waveshare/WeatherSolarOutput.svg

#echo "Display on epaper"

#python3 /home/neal/scripts/waveshare/display.py /home/neal/scripts/waveshare/screen-output.png

#!/usr/bin/env bash
set -euo pipefail

# --- Paths ---
APP_DIR="/home/neal/apps/utility"
WS_DIR="$APP_DIR/waveshare"

# If you still have env vars in waveshare/env.sh, source the new copy here:
# [ -f "$WS_DIR/env.sh" ] && . "$WS_DIR/env.sh"

# Ensure Python can find the vendored Waveshare driver
export PYTHONPATH="$WS_DIR/lib:$PYTHONPATH"

# Use the project's venv tools
PY="$APP_DIR/.venv/bin/python"
CAIROS="$APP_DIR/.venv/bin/cairosvg"   # will exist after installing cairosvg in the venv

echo "Add weather info"
"$PY" "$WS_DIR/WeatherSolar.py"

echo "Export to PNG"
WAVESHARE_WIDTH=800
WAVESHARE_HEIGHT=480
SVG_IN="$WS_DIR/WeatherSolarOutput.svg"
PNG_OUT="$WS_DIR/screen-output.png"

# Render SVG -> PNG
"$CAIROS" -u -o "$PNG_OUT" -f png --dpi 300 \
  --output-width "$WAVESHARE_WIDTH" --output-height "$WAVESHARE_HEIGHT" \
  "$SVG_IN"

echo "Display on epaper"
"$PY" "$WS_DIR/display.py" "$PNG_OUT"

