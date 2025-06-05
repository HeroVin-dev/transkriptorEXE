# Transkriptor

A simple GUI tool to convert audio files to text using modern libraries.

## Requirements
- Python 3.8+
- [PyQt5](https://pypi.org/project/PyQt5/)
- [vosk](https://pypi.org/project/vosk/)
- [openai-whisper](https://pypi.org/project/openai-whisper/)

Install dependencies and download a Vosk model (for example `vosk-model-small-ru`):
```bash
pip install PyQt5 vosk openai-whisper
# Download a model and unpack it to a folder named 'model'
```

## Usage
Run the application with Python:
```bash
python transkriptor.py
```
Select an audio file (WAV, FLAC, AIFF or MP3) and press **Transcribe** to see the recognized text.
