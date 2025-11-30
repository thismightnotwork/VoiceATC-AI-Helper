#!/usr/bin/env python3
"""
VoiceATC AI Helper - Speech-to-text powered ATC phrase recognition

This helper application:
1. Listens to user speech via microphone
2. Uses Vosk or Whisper for accurate speech recognition
3. Maps recognized speech to canonical ATC phrases
4. Outputs clean speech via TTS to a virtual microphone
5. VoiceATC receives perfect audio for 100% recognition
"""

import json
import logging
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional
import pyttsx3

try:
    from vosk import Model, KaldiRecognizer
    import pyaudio
except ImportError:
    print("Error: Required packages not installed.")
    print("Run: pip install -r requirements.txt")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class VoiceATCHelper:
    """Main helper application for VoiceATC AI integration."""

    def __init__(self, config_path: str = "config/voiceatc_config.json"):
        """Initialize the helper with configuration."""
        self.config = self._load_config(config_path)
        self.phrase_mappings = self._load_phrase_mappings()
        self.recognizer = None
        self.audio = None
        self.tts_engine = pyttsx3.init()
        self._setup_recognizer()
        logger.info("VoiceATC Helper initialized successfully")

    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file."""
        if not os.path.exists(config_path):
            logger.error(f"Config file not found: {config_path}")
            sys.exit(1)
        with open(config_path) as f:
            return json.load(f)

    def _load_phrase_mappings(self) -> Dict:
        """Load ATC phrase mappings from JSON file."""
        mappings_path = "config/phrase_mappings.json"
        if not os.path.exists(mappings_path):
            logger.error(f"Phrase mappings file not found: {mappings_path}")
            return {}
        with open(mappings_path) as f:
            data = json.load(f)
            return data.get("mappings", [])

    def _setup_recognizer(self):
        """Setup Vosk speech recognizer."""
        try:
            model_path = self.config.get("vosk_model_path")
            if not os.path.exists(model_path):
                logger.error(f"Vosk model not found: {model_path}")
                logger.info("Download from: https://alphacephei.com/vosk/models")
                sys.exit(1)
            self.recognizer = Model(model_path)
            self.audio = pyaudio.PyAudio()
            logger.info("Recognizer setup complete")
        except Exception as e:
            logger.error(f"Failed to setup recognizer: {e}")
            sys.exit(1)

    def match_phrase(self, recognized_text: str) -> Optional[str]:
        """Match recognized text to a canonical ATC phrase."""
        text_lower = recognized_text.lower().strip()
        for mapping in self.phrase_mappings:
            for variant in mapping.get("variants", []):
                if variant.lower() in text_lower or text_lower in variant.lower():
                    return mapping["canonical"]
        return None

    def speak_phrase(self, phrase: str):
        """Synthesize and output phrase via TTS to virtual cable."""
        try:
            voice_name = self.config.get("tts_voice", "Microsoft Zira Desktop")
            voices = self.tts_engine.getProperty('voices')
            for voice in voices:
                if voice_name in voice.name:
                    self.tts_engine.setProperty('voice', voice.id)
                    break
            self.tts_engine.say(phrase)
            self.tts_engine.runAndWait()
            logger.info(f"Spoke: {phrase}")
        except Exception as e:
            logger.error(f"TTS error: {e}")

    def listen_and_process(self):
        """Main loop: listen for speech, process, and output."""
        try:
            stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=4096
            )
            stream.start_stream()
            recognizer = KaldiRecognizer(self.recognizer, 16000)
            logger.info("Listening... Speak into microphone (Ctrl+C to stop)")
            while True:
                data = stream.read(4096, exception_on_overflow=False)
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    recognized = result.get("result", [])
                    if recognized:
                        text = " ".join([r["conf"] for r in recognized])
                        canonical = self.match_phrase(text)
                        if canonical:
                            logger.info(f"Recognized: {text} => {canonical}")
                            self.speak_phrase(canonical)
                        else:
                            logger.info(f"No match for: {text}")
        except KeyboardInterrupt:
            logger.info("Shutting down...")
        finally:
            stream.stop_stream()
            stream.close()
            self.audio.terminate()

def main():
    """Entry point for the application."""
    try:
        helper = VoiceATCHelper()
        helper.listen_and_process()
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
