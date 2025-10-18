#!/bin/bash
# Test script to verify the translation solution works
# Run this on a machine with internet access

echo "================================"
echo "Subtitle Translation Test Script"
echo "================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ ERROR: Python 3 is not installed"
    exit 1
fi
echo "✓ Python 3 found: $(python3 --version)"

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ ERROR: pip3 is not installed"
    exit 1
fi
echo "✓ pip3 found"

# Check for subtitle files
SRT_COUNT=$(ls -1 *.srt 2>/dev/null | grep -v "pt-BR" | wc -l)
if [ "$SRT_COUNT" -eq 0 ]; then
    echo "❌ ERROR: No .srt files found in current directory"
    exit 1
fi
echo "✓ Found $SRT_COUNT subtitle file(s) to translate"

# Check if translations already exist
TRANSLATED_COUNT=$(ls -1 *.pt-BR.srt 2>/dev/null | wc -l)
if [ "$TRANSLATED_COUNT" -gt 0 ]; then
    echo "⚠ Warning: $TRANSLATED_COUNT translation(s) already exist"
    echo "   These will be skipped"
fi

echo ""
echo "Installing required package..."
pip3 install -q deep-translator

if [ $? -ne 0 ]; then
    echo "❌ ERROR: Failed to install deep-translator"
    exit 1
fi
echo "✓ deep-translator installed"

echo ""
echo "Testing translation capability..."
python3 << 'EOF'
try:
    from deep_translator import GoogleTranslator
    translator = GoogleTranslator(source='en', target='pt')
    result = translator.translate("Hello, world!")
    print(f"✓ Translation test successful: 'Hello, world!' → '{result}'")
except Exception as e:
    print(f"❌ Translation test failed: {e}")
    exit(1)
EOF

if [ $? -ne 0 ]; then
    echo "❌ ERROR: Translation test failed (check internet connection)"
    exit 1
fi

echo ""
echo "================================"
echo "Everything ready!"
echo "================================"
echo ""
echo "To translate all subtitle files, run:"
echo "  python3 translate_with_deep_translator.py"
echo ""
echo "Estimated time: 5-10 minutes per file"
echo "Total estimated time: 40-80 minutes for all $SRT_COUNT files"
echo ""
