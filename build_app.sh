#!/bin/zsh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
APP_NAME="Dimo Extractor.app"
BUILD_DIR="$SCRIPT_DIR/dist"
APP_PATH="$BUILD_DIR/$APP_NAME"
JXA_SOURCE="$SCRIPT_DIR/Drag TXT Here.js"
PY_SOURCE="$SCRIPT_DIR/extract_dimo_quotes.py"
PLIST_BUDDY="/usr/libexec/PlistBuddy"

set_plist_string() {
  local key="$1"
  local value="$2"

  if ! "$PLIST_BUDDY" -c "Set :$key $value" "$APP_PATH/Contents/Info.plist" 2>/dev/null; then
    "$PLIST_BUDDY" -c "Add :$key string $value" "$APP_PATH/Contents/Info.plist"
  fi
}

if [ ! -f "$JXA_SOURCE" ]; then
  echo "未找到 JXA 源文件: $JXA_SOURCE" >&2
  exit 1
fi

if [ ! -f "$PY_SOURCE" ]; then
  echo "未找到 Python 源文件: $PY_SOURCE" >&2
  exit 1
fi

rm -rf "$APP_PATH"
mkdir -p "$BUILD_DIR"

osacompile -l JavaScript -o "$APP_PATH" "$JXA_SOURCE"
cp "$PY_SOURCE" "$APP_PATH/Contents/Resources/extract_dimo_quotes.py"
chmod 755 "$APP_PATH/Contents/Resources/extract_dimo_quotes.py"

if [ -x "$PLIST_BUDDY" ]; then
  set_plist_string "CFBundleName" "Dimo Extractor"
  set_plist_string "CFBundleDisplayName" "Dimo Extractor"
  set_plist_string "CFBundleIdentifier" "com.klaithz.dimo-extractor"
fi

echo "Built: $APP_PATH"
