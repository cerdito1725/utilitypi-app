#!/usr/bin/env bash
set -euo pipefail

APP_DIR="/home/neal/apps/utility"
WS_DIR="$APP_DIR/waveshare"

# If you still keep env vars in waveshare/env.sh, source it:
# [ -f "$WS_DIR/env.sh" ] && . "$WS_DIR/env.sh"

# Make sure Python can find the vendored Waveshare ePaper driver
export PYTHONPATH="$WS_DIR/lib:$PYTHONPATH"

# Use the project's venv tools
PY="$APP_DIR/.venv/bin/python"
CAIROS="$APP_DIR/.venv/bin/cairosvg"   # falls back to system cairosvg if venv one not present
[ -x "$CAIROS" ] || CAIROS="/usr/bin/cairosvg"

echo "Add weather info"
/usr/bin/env -i PATH="/usr/bin:/bin" PYTHONPATH="$PYTHONPATH" "$PY" "$WS_DIR/WeatherSolar.py"

echo "Export to PNG"
WAVESHARE_WIDTH=800
WAVESHARE_HEIGHT=480
SVG_IN="$WS_DIR/WeatherSolarOutput.svg"
PNG_OUT="$WS_DIR/screen-output.png"

"$CAIROS" -u -o "$PNG_OUT" -f png --dpi 300 \
  --output-width "$WAVESHARE_WIDTH" --output-height "$WAVESHARE_HEIGHT" \
  "$SVG_IN"

echo "Display on epaper"
/usr/bin/env -i PATH="/usr/bin:/bin" PYTHONPATH="$PYTHONPATH" "$PY" "$WS_DIR/display.py" "$PNG_OUT"

echo "Done."
