# How to Translate the Subtitles

This document provides step-by-step instructions for translating the English subtitle files to Brazilian Portuguese.

## The Challenge

This environment has network restrictions that prevent:
- Accessing Google Translate API
- Downloading translation models from Hugging Face
- Using any external translation services

## Solution Options

### Option 1: Use the Provided Script on a Machine with Internet (RECOMMENDED)

1. **Clone this repository** on a computer with internet access
2. **Install Python 3** if not already installed
3. **Install the translation library:**
   ```bash
   pip install deep-translator
   ```
4. **Run the translation script:**
   ```bash
   cd legendas
   python3 translate_with_deep_translator.py
   ```
5. **Wait for completion** (estimated 30-60 minutes for all 8 files)
6. **Commit and push** the translated files back to the repository

### Option 2: Use Subtitle Edit (Free Software)

[Subtitle Edit](https://github.com/SubtitleEdit/subtitleedit) is a free, open-source subtitle editor with built-in translation.

1. **Download and install Subtitle Edit**
2. **Open each .srt file**
3. **Use Auto-Translate feature:**
   - Tools → Auto-translate
   - Select: English → Portuguese
   - Choose translation service (Google Translate)
4. **Review and save** with `.pt-BR.srt` suffix
5. **Repeat for all 8 files**

### Option 3: Professional Translation Service

Given the authorization document provided (Auth.pdf), consider hiring:
- Professional subtitle translators
- Translation agencies specializing in media content
- Freelance translators on platforms like Upwork or Fiverr

Expected cost: $50-200 USD for all 8 episodes depending on quality level.

### Option 4: MarianMT Model (Requires Initial Internet)

If you have a machine with internet for the first run:

1. **Install dependencies:**
   ```bash
   pip install transformers torch sentencepiece
   ```
2. **Run the MarianMT script:**
   ```bash
   python3 translate_with_marian.py
   ```
3. The first run will download models (~300MB)
4. Subsequent runs work offline

## Expected Output

Each original file will get a translated version:
- `Naked.and.Afraid.Apocalypse.S01E01.1080p.HEVC.x265-MeGusta.srt`
- `Naked.and.Afraid.Apocalypse.S01E01.1080p.HEVC.x265-MeGusta.pt-BR.srt` ← new

## File Statistics

- **Total files:** 8
- **Total subtitle entries:** ~14,370
- **Estimated translation time:**
  - Automated (with network): 30-60 minutes
  - Manual with tools: 4-8 hours
  - Professional service: 1-3 days turnaround

## Quality Assurance

After translation:
1. Spot-check several entries for accuracy
2. Watch a few minutes of video with subtitles
3. Verify timing hasn't been affected
4. Check for proper Portuguese grammar and spelling

## Scripts Provided in This Repository

1. **translate_with_deep_translator.py** - Best option, uses Google Translate
2. **translate_with_marian.py** - Uses offline-capable model (after first download)
3. **translate_subtitles.py** - Framework supporting multiple backends
4. **direct_translate.py** - Helper for custom translation workflows

## Questions?

If you need help or have questions about the translation process, please:
1. Open an issue in this repository
2. Include details about your approach and any error messages
3. Mention which option you're attempting

## Authorization

Translation is authorized as per the document in `Auth.pdf`.
