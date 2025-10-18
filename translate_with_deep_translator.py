#!/usr/bin/env python3
"""
Complete subtitle translation script using deep-translator library.
This script translates English subtitle files (.srt) to Brazilian Portuguese (pt-BR).

Requirements:
    pip install deep-translator

Usage:
    python3 translate_with_deep_translator.py

This will translate all .srt files in the current directory that don't already have
pt-BR translations.
"""

import re
import time
from pathlib import Path
from deep_translator import GoogleTranslator


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
    Translate text to Brazilian Portuguese with retry logic.
    Handles HTML tags and formatting commonly found in subtitles.
    """
    if not text or not text.strip():
        return text
    
    # Preserve HTML tags like <i>, </i>, <b>, </b>
    html_tag_pattern = r'(<[^>]+>)'
    parts = re.split(html_tag_pattern, text)
    
    translated_parts = []
    for part in parts:
        # Skip empty parts
        if not part.strip():
            translated_parts.append(part)
            continue
            
        # Keep HTML tags as-is
        if re.match(html_tag_pattern, part):
            translated_parts.append(part)
            continue
        
        # Translate actual text content
        for attempt in range(max_retries):
            try:
                # Translate to Portuguese (pt = Portuguese, will be Brazilian Portuguese)
                translation = translator.translate(part)
                translated_parts.append(translation)
                break
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"    Translation attempt {attempt + 1} failed, retrying... ({str(e)})")
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    print(f"    Translation failed after {max_retries} attempts: {str(e)}")
                    translated_parts.append(part)  # Return original on failure
                    break
    
    return ''.join(translated_parts)


def write_srt_file(filepath, subtitles):
    """Write subtitles to an SRT file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        for subtitle in subtitles:
            f.write(f"{subtitle['index']}\n")
            f.write(f"{subtitle['timestamp']}\n")
            f.write(f"{subtitle['text']}\n\n")


def translate_subtitle_file(input_file, output_file):
    """
    Translate an entire subtitle file from English to Brazilian Portuguese.
    """
    print(f"\nTranslating: {input_file}")
    print(f"Output: {output_file}")
    
    # Parse the SRT file
    subtitles = parse_srt_file(input_file)
    print(f"Found {len(subtitles)} subtitle entries")
    
    # Initialize translator (English to Portuguese)
    translator = GoogleTranslator(source='en', target='pt')
    
    # Translate each subtitle
    translated_subtitles = []
    for i, subtitle in enumerate(subtitles, 1):
        if i % 50 == 0:
            print(f"  Progress: {i}/{len(subtitles)} ({i*100//len(subtitles)}%)")
        
        translated_text = translate_text(subtitle['text'], translator)
        
        translated_subtitles.append({
            'index': subtitle['index'],
            'timestamp': subtitle['timestamp'],
            'text': translated_text
        })
        
        # Small delay to avoid rate limiting (every 10 translations)
        if i % 10 == 0:
            time.sleep(0.5)
    
    # Write translated subtitles to output file
    write_srt_file(output_file, translated_subtitles)
    
    print(f"✓ Translation complete: {output_file}")
    print(f"  Total entries translated: {len(translated_subtitles)}")


def main():
    """
    Main function to translate all subtitle files in the current directory.
    """
    print("="*60)
    print("Subtitle Translation Script - English to Brazilian Portuguese")
    print("="*60)
    
    # Get all .srt files in the current directory
    srt_files = sorted(Path('.').glob('*.srt'))
    
    # Filter out files that already have pt-BR in the name
    srt_files = [f for f in srt_files if '.pt-BR.' not in f.name]
    
    if not srt_files:
        print("\nNo subtitle files found to translate!")
        print("(Files with '.pt-BR.' in the name are skipped)")
        return
    
    print(f"\nFound {len(srt_files)} subtitle file(s) to translate:\n")
    for i, srt_file in enumerate(srt_files, 1):
        print(f"  {i}. {srt_file.name}")
    
    print("\nStarting translation process...")
    print("This may take some time depending on file sizes and network speed.\n")
    
    start_time = time.time()
    
    for srt_file in srt_files:
        # Create output filename with pt-BR suffix
        output_name = srt_file.stem + '.pt-BR' + srt_file.suffix
        output_file = srt_file.parent / output_name
        
        # Skip if output file already exists
        if output_file.exists():
            print(f"\nSkipping {srt_file.name} - translation already exists")
            continue
        
        translate_subtitle_file(srt_file, output_file)
    
    elapsed_time = time.time() - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    
    print("\n" + "="*60)
    print("All translations completed!")
    print(f"Total time: {minutes}m {seconds}s")
    print("="*60)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTranslation interrupted by user.")
    except Exception as e:
        print(f"\n\nError occurred: {str(e)}")
        import traceback
        traceback.print_exc()
