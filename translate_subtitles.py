#!/usr/bin/env python3
"""
Script to translate subtitle files (.srt) from English to Brazilian Portuguese (pt-BR)

This script requires internet access to translation services. If running in an environment
without internet access, you'll need to use an alternative translation method such as:
1. A local translation model (e.g., Argos Translate with pre-downloaded models)
2. A translation API with custom endpoint configuration
3. Manual translation with assistance from a language model
"""

import re
import sys
import time
from pathlib import Path

# Try multiple translation backends
TRANSLATION_BACKEND = None

try:
    from deep_translator import GoogleTranslator
    TRANSLATION_BACKEND = "deep_translator"
except ImportError:
    pass

if TRANSLATION_BACKEND is None:
    try:
        from googletrans import Translator as GoogleTrans
        TRANSLATION_BACKEND = "googletrans"
    except ImportError:
        pass

if TRANSLATION_BACKEND is None:
    print("ERROR: No translation library available.")
    print("Please install one of: deep-translator, googletrans")
    print("  pip install deep-translator")
    print("  pip install googletrans==4.0.0-rc1")
    sys.exit(1)


def parse_srt_file(filepath):
    """
    Parse an SRT subtitle file and return a list of subtitle entries.
    Each entry is a dict with: index, timestamp, text
    """
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        content = f.read()
    
    # Split by double newlines to get individual subtitle blocks
    blocks = re.split(r'\n\n+', content.strip())
    
    subtitles = []
    for block in blocks:
        if not block.strip():
            continue
        
        lines = block.strip().split('\n')
        if len(lines) < 2:
            continue
        
        # First line is the index
        index = lines[0].strip()
        
        # Second line is the timestamp
        timestamp = lines[1].strip()
        
        # Remaining lines are the subtitle text
        text = '\n'.join(lines[2:])
        
        subtitles.append({
            'index': index,
            'timestamp': timestamp,
            'text': text
        })
    
    return subtitles


def translate_text(text, translator, max_retries=3):
    """
    Translate text to Brazilian Portuguese with retry logic
    """
    for attempt in range(max_retries):
        try:
            # Translate to Portuguese (Brazil)
            translation = translator.translate(text, src='en', dest='pt')
            return translation.text
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"  Translation attempt {attempt + 1} failed, retrying... ({str(e)})")
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                print(f"  Translation failed after {max_retries} attempts: {str(e)}")
                return text  # Return original text if translation fails


def translate_subtitles(input_file, output_file):
    """
    Translate an entire subtitle file from English to Brazilian Portuguese
    """
    print(f"\nTranslating: {input_file}")
    print(f"Output: {output_file}")
    
    # Parse the SRT file
    subtitles = parse_srt_file(input_file)
    print(f"Found {len(subtitles)} subtitle entries")
    
    # Initialize translator
    translator = Translator()
    
    # Translate each subtitle
    translated_subtitles = []
    for i, subtitle in enumerate(subtitles, 1):
        if i % 10 == 0:
            print(f"  Progress: {i}/{len(subtitles)}")
        
        translated_text = translate_text(subtitle['text'], translator)
        
        translated_subtitles.append({
            'index': subtitle['index'],
            'timestamp': subtitle['timestamp'],
            'text': translated_text
        })
        
        # Small delay to avoid rate limiting
        if i % 5 == 0:
            time.sleep(1)
    
    # Write translated subtitles to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        for subtitle in translated_subtitles:
            f.write(f"{subtitle['index']}\n")
            f.write(f"{subtitle['timestamp']}\n")
            f.write(f"{subtitle['text']}\n\n")
    
    print(f"✓ Translation complete: {output_file}")


def main():
    """
    Main function to translate all subtitle files
    """
    # Get all .srt files in the current directory
    srt_files = sorted(Path('.').glob('*.srt'))
    
    # Filter out files that already have pt-BR in the name
    srt_files = [f for f in srt_files if '.pt-BR.' not in f.name]
    
    if not srt_files:
        print("No subtitle files found to translate!")
        return
    
    print(f"Found {len(srt_files)} subtitle file(s) to translate")
    
    for srt_file in srt_files:
        # Create output filename with pt-BR suffix
        output_name = srt_file.stem + '.pt-BR' + srt_file.suffix
        output_file = srt_file.parent / output_name
        
        # Skip if output file already exists
        if output_file.exists():
            print(f"\nSkipping {srt_file.name} - translation already exists")
            continue
        
        translate_subtitles(srt_file, output_file)
    
    print("\n" + "="*60)
    print("All translations completed!")
    print("="*60)


if __name__ == '__main__':
    main()
