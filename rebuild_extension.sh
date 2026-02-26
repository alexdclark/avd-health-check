#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

EXT_NAME="avd-health-check"
WHEEL_GLOB="dist/avd_health_check-*.whl"

if ! command -v az >/dev/null 2>&1; then
  echo "Error: Azure CLI (az) is not installed or not on PATH."
  exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "Error: python3 is not installed or not on PATH."
  exit 1
fi

export AZURE_CONFIG_DIR="${AZURE_CONFIG_DIR:-$SCRIPT_DIR/.azure}"
mkdir -p "$AZURE_CONFIG_DIR"
mkdir -p dist

echo "Building wheel..."
rm -f $WHEEL_GLOB
python3 -m pip wheel --no-build-isolation . -w dist

WHEEL_PATH="$(ls -t $WHEEL_GLOB | head -n 1)"
if [[ -z "${WHEEL_PATH:-}" ]]; then
  echo "Error: No wheel was produced."
  exit 1
fi

if az extension show -n "$EXT_NAME" >/dev/null 2>&1; then
  echo "Removing existing extension: $EXT_NAME"
  az extension remove -n "$EXT_NAME" >/dev/null
fi

echo "Installing extension from: $WHEEL_PATH"
az extension add --source "$WHEEL_PATH" -y >/dev/null

echo "Done."
echo "Config dir: $AZURE_CONFIG_DIR"
echo "Installed wheel: $WHEEL_PATH"
