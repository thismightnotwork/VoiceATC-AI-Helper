# VoiceATC-AI-Helper

A free, offline AI speech-to-text helper for VoiceATC that improves ATC phrase recognition accuracy using Whisper or Vosk and virtual audio cables.

## Overview

VoiceATC currently relies on Windows Speech Recognition, which has limited accuracy for ATC-specific phraseology. This helper application uses modern AI speech-to-text engines to recognize your speech with higher accuracy, then feeds clean, synthetic ATC phrases back into VoiceATC through a virtual audio cable.

**Why this works:**
- VoiceATC's Windows STT still handles the final recognition, but now receives perfect, well-enunciated synthetic speech instead of your raw input
- No modifications needed to VoiceATC itself
- Runs as an independent companion application
- Fully offline (no API calls, no data sent anywhere)

## How it works

```
You speak → AI STT engine (Whisper/Vosk) → Phrase mapping → TTS synthesis → Virtual cable → VoiceATC
```

1. **Audio Capture**: Helper app listens to your microphone (optionally with push-to-talk)
2. **STT Recognition**: Speech is sent to a local Whisper or Vosk model
3. **Phrase Mapping**: Recognized text is normalized and matched to a canonical ATC phrase
4. **TTS Output**: The canonical phrase is converted to clean speech via Windows TTS
5. **Virtual Cable**: Synthetic audio is routed through VB-Audio Virtual Cable to VoiceATC
6. **VoiceATC**: Windows STT inside VoiceATC recognizes the perfect synthetic phrase with near-100% accuracy

## Requirements

### Software
- Python 3.8+
- Windows 10/11
- VoiceATC (already installed and working)

### Python packages
```bash
pip install pyaudio vosk  # For Vosk engine
# OR
pip install pyaudio openai-whisper  # For Whisper engine
```

### System setup
1. **Install VB-Audio Virtual Cable**
   - Download from: https://vb-audio.com/Cable/
   - Install and restart Windows

2. **Configure Windows audio**
   - Right-click your Speaker icon → Open Volume mixer
   - Set default microphone to: "Cable Output (VB-Audio Virtual Cable)"

3. **Download STT model** (if using Vosk)
   - Download English model from: https://alphacephei.com/vosk/models
   - Extract to `models/vosk-model-en-us-0.42-gigaspeech` folder

## Installation

1. **Clone this repository**
   ```bash
   git clone https://github.com/yourusername/VoiceATC-AI-Helper.git
   cd VoiceATC-AI-Helper
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the helper**
   - Edit `config/voiceatc_config.json` to select your STT engine and adjust settings
   - Add/customize ATC phrases in `config/phrase_mappings.json`

## Usage

### Start the helper app
```bash
python src/voiceatc_helper.py
```

### In VoiceATC
1. Open VoiceATC
2. Go to Settings → Audio → Microphone
3. Select: "Cable Output (VB-Audio Virtual Cable)"
4. Test with push-to-talk; your speech will be transcribed and converted to clean ATC phrases

## Configuration

### `config/voiceatc_config.json`
```json
{
  "stt_engine": "vosk",  // or "whisper"
  "vosk_model_path": "models/vosk-model-en-us-0.42-gigaspeech",
  "whisper_model_size": "tiny",  // tiny, base, small, medium, large
  "push_to_talk_key": "shift",  // or "v", "space", etc.
  "tts_voice": "Microsoft Zira Desktop",  // Windows voice name
  "output_device": "CABLE Input (VB-Audio Virtual Cable)",
  "confidence_threshold": 0.7,
  "auto_normalize_numbers": true
}
```

### `config/phrase_mappings.json`
Map natural speech variants to canonical ATC phrases:
```json
{
  "mappings": [
    {
      "variants": [
        "ready for departure runway two three left",
        "ready for takeoff two three left",
        "ready to depart runway 23 left"
      ],
      "canonical": "tower ready for departure runway two three left"
    },
    {
      "variants": [
        "climb maintain five thousand",
        "climb and maintain five thousand feet",
        "climb to five thousand"
      ],
      "canonical": "climb maintain five thousand feet"
    }
  ]
}
```

## Troubleshooting

### No audio from helper?
- Check "Cable Output" is set as your microphone in Windows Sound settings
- Verify VB-Audio Cable is installed correctly
- Try unplugging and replugging the virtual cable

### STT not recognizing speech?
- Ensure your microphone volume is adequate (check Windows Sound input levels)
- Try speaking more clearly and at a normal pace
- Verify Vosk/Whisper model is installed and model path is correct
- For Whisper: first run downloads the model (~1-2 GB depending on size)

### VoiceATC still not recognizing phrases?
- Check that helper app is running and showing output
- Verify the canonical phrase in `phrase_mappings.json` matches what VoiceATC expects
- Test Windows STT directly with Cortana to ensure baseline recognition works

### High latency?
- Use Vosk instead of Whisper (faster, lower CPU usage)
- Use a smaller Whisper model ("tiny" or "base")
- Ensure your system has adequate CPU/RAM available
- Reduce audio buffer size in config if available

## Performance

| Engine | Model | CPU | Memory | Latency |
|--------|-------|-----|--------|----------|
| Vosk | default | ~15% | 100MB | 500ms-1s |
| Whisper | tiny | ~40% | 500MB | 1-2s |
| Whisper | base | ~60% | 800MB | 2-3s |
| Whisper | small | ~80% | 1.2GB | 3-4s |

*Approximate values on a mid-range system (i5-9400, 16GB RAM)*

## Project structure

```
VoiceATC-AI-Helper/
├── src/
│   ├── voiceatc_helper.py          # Main application
│   ├── stt_engines.py              # Vosk/Whisper wrappers
│   ├── phrase_matcher.py           # Phrase mapping logic
│   └── audio_io.py                 # Audio capture/output
├── config/
│   ├── voiceatc_config.json        # Main configuration
│   └── phrase_mappings.json        # ATC phrase database
├── models/                         # Vosk models (not included, download separately)
├── requirements.txt                # Python dependencies
└── README.md
```

## Contributing

Contributions welcome! Especially:
- Additional ATC phrase mappings
- Language support (French, German, Spanish, etc.)
- Improved phrase matching algorithms
- Performance optimizations
- Testing on various Windows versions

## License

MIT License - See LICENSE file for details

## Disclaimer

This is a hobby/educational project. It is not suitable for real aviation use. Always follow official air traffic control procedures and use certified equipment.

## Credits

- Vosk: https://alphacephei.com/vosk/
- OpenAI Whisper: https://openai.com/research/whisper
- VB-Audio Virtual Cable: https://vb-audio.com/Cable/
- VoiceATC: (original simulator)
