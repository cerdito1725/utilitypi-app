#!/usr/bin/env bash
set -euo pipefail

APP_DIR="/home/neal/apps/utility"
WS_DIR="$APP_DIR/waveshare"

# Load your provider + location config
[ -f "$WS_DIR/env.sh" ] && . "$WS_DIR/env.sh"

# Make Waveshare driver importable
export PYTHONPATH="$WS_DIR/lib"

PY="$APP_DIR/.venv/bin/python"
CAIROS="$APP_DIR/.venv/bin/cairosvg"; [ -x "$CAIROS" ] || CAIROS="/usr/bin/cairosvg"

echo "Provider: ${WEATHER_MET_EIREANN:-0}  Lat/Lon: ${WEATHER_LATITUDE:-?},${WEATHER_LONGITUDE:-?}"

echo "Add weather info"
"$PY" "$WS_DIR/WeatherSolar.py"

echo "Export to PNG"
WAVESHARE_WIDTH=800
WAVESHARE_HEIGHT=480
SVG_IN="$WS_DIR/WeatherSolarOutput.svg"
PNG_OUT="$WS_DIR/screen-output.png"

"$CAIROS" -u -o "$PNG_OUT" -f png --dpi 300 \
  --output-width "$WAVESHARE_WIDTH" --output-height "$WAVESHARE_HEIGHT" \
  "$SVG_IN"

echo "Display on ePaper"
"$PY" "$WS_DIR/display.py" "$PNG_OUT"

echo "Done."
