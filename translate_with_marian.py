#!/usr/bin/env python3
"""
Alternative translation script using transformers library with MarianMT models.
This can work offline once models are downloaded.

Installation:
    pip install transformers torch sentencepiece

First run will download models (~300MB), subsequent runs work offline.
"""

import re
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

def parse_srt_file(filepath):
    """Parse SRT file."""
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        content = f.read()
    
    blocks = re.split(r'\n\n+', content.strip())
    subtitles = []
    
    for block in blocks:
        if not block.strip():
            continue
        lines = block.strip().split('\n')
        if len(lines) < 2:
            continue
        
        subtitles.append({
            'index': lines[0].strip(),
            'timestamp': lines[1].strip(),
            'text': '\n'.join(lines[2:])
        })
    
    return subtitles


def translate_with_marian(text, model, tokenizer, max_length=512):
    """Translate text using MarianMT model."""
    if not text or not text.strip():
        return text
    
    # Preserve HTML tags
    html_tag_pattern = r'(<[^>]+>)'
    parts = re.split(html_tag_pattern, text)
    
    translated_parts = []
    for part in parts:
        if not part.strip() or re.match(html_tag_pattern, part):
            translated_parts.append(part)
            continue
        
        # Translate
        try:
            inputs = tokenizer(part, return_tensors="pt", padding=True, truncation=True, max_length=max_length)
            outputs = model.generate(**inputs)
            translated = tokenizer.decode(outputs[0], skip_special_tokens=True)
            translated_parts.append(translated)
        except Exception as e:
            print(f"    Translation error: {e}")
            translated_parts.append(part)
    
    return ''.join(translated_parts)


def write_srt_file(filepath, subtitles):
    """Write SRT file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        for subtitle in subtitles:
            f.write(f"{subtitle['index']}\n")
            f.write(f"{subtitle['timestamp']}\n")
            f.write(f"{subtitle['text']}\n\n")


def translate_subtitle_file_marian(input_file, output_file):
    """Translate subtitle file using MarianMT."""
    try:
        from transformers import MarianMTModel, MarianTokenizer
    except ImportError:
        print("ERROR: transformers library not installed")
        print("Install with: pip install transformers torch sentencepiece")
        return False
    
    print(f"\nTranslating: {input_file}")
    print(f"Output: {output_file}")
    
    # Load model and tokenizer
    print("Loading translation model (this may take a while on first run)...")
    model_name = "Helsinki-NLP/opus-mt-en-pt"
    
    try:
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
        print("Model loaded successfully!")
    except Exception as e:
        print(f"ERROR: Could not load model: {e}")
        print("This requires internet connection on first run to download the model.")
        return False
    
    # Parse subtitle file
    subtitles = parse_srt_file(input_file)
    print(f"Found {len(subtitles)} subtitle entries")
    
    # Translate
    translated_subtitles = []
    for i, subtitle in enumerate(subtitles, 1):
        if i % 50 == 0:
            print(f"  Progress: {i}/{len(subtitles)} ({i*100//len(subtitles)}%)")
        
        translated_text = translate_with_marian(subtitle['text'], model, tokenizer)
        translated_subtitles.append({
            'index': subtitle['index'],
            'timestamp': subtitle['timestamp'],
            'text': translated_text
        })
    
    # Write output
    write_srt_file(output_file, translated_subtitles)
    print(f"✓ Translation complete: {output_file}")
    return True


def main():
    """Main function."""
    print("="*60)
    print("Subtitle Translation with MarianMT (Offline-capable)")
    print("="*60)
    
    srt_files = sorted(Path('.').glob('*.srt'))
    srt_files = [f for f in srt_files if '.pt-BR.' not in f.name]
    
    if not srt_files:
        print("\nNo subtitle files found!")
        return
    
    print(f"\nFound {len(srt_files)} file(s) to translate\n")
    
    for srt_file in srt_files:
        output_name = srt_file.stem + '.pt-BR' + srt_file.suffix
        output_file = srt_file.parent / output_name
        
        if output_file.exists():
            print(f"\nSkipping {srt_file.name} - already translated")
            continue
        
        success = translate_subtitle_file_marian(srt_file, output_file)
        if not success:
            print(f"Failed to translate {srt_file.name}")
            break
    
    print("\n" + "="*60)
    print("Translation process complete!")
    print("="*60)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()
