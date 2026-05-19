#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEVELOPER_DIR="${DEVELOPER_DIR:-/Applications/Xcode.app/Contents/Developer}"

if [[ ! -d "$DEVELOPER_DIR" ]]; then
  echo "Xcode was not found at $DEVELOPER_DIR." >&2
  echo "Install Xcode or set DEVELOPER_DIR to your Xcode app path." >&2
  exit 1
fi

export DEVELOPER_DIR

PROJECT="$ROOT/ios/Thrifty/Thrifty.xcodeproj"
SCHEME="Thrifty"
IPHONE_DESTINATION="platform=iOS Simulator,name=iPhone 16e,OS=26.3.1"
IPAD_DESTINATION="platform=iOS Simulator,name=iPad Air 11-inch (M3),OS=26.3.1"

xcodebuild \
  -project "$PROJECT" \
  -scheme "$SCHEME" \
  -destination "$IPHONE_DESTINATION" \
  -configuration Debug \
  -derivedDataPath "$ROOT/ios/.derivedData-iphone" \
  build

xcodebuild \
  -project "$PROJECT" \
  -scheme "$SCHEME" \
  -destination "$IPAD_DESTINATION" \
  -configuration Debug \
  -derivedDataPath "$ROOT/ios/.derivedData-ipad" \
  build

echo "iPhone and iPad simulator builds passed."
