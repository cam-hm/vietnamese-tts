"""
TTS Service - Google Cloud Text-to-Speech wrapper
"""
from google.cloud import texttospeech
from typing import Optional

# Available BBC documentary-style voices
# Organized by type: Studio (broadcast), Chirp3-HD (newest), Neural2 (standard)
AVAILABLE_VOICES = {
    # 🎬 STUDIO VOICES - Designed for broadcast/documentary narration
    "en-GB-Studio-B": {"name": "🎬 British Male (Studio) - Documentary", "gender": "MALE", "type": "studio"},
    "en-GB-Studio-C": {"name": "🎬 British Female (Studio) - Documentary", "gender": "FEMALE", "type": "studio"},
    "en-US-Studio-O": {"name": "🎬 American Male (Studio) - Documentary", "gender": "MALE", "type": "studio"},
    "en-US-Studio-Q": {"name": "🎬 American Female (Studio) - Documentary", "gender": "FEMALE", "type": "studio"},
    
    # 🌟 CHIRP3-HD VOICES - Newest, most natural voices
    "en-GB-Chirp3-HD-Charon": {"name": "🌟 British (Charon) - Ultra Natural", "gender": "NEUTRAL", "type": "chirp3"},
    "en-GB-Chirp3-HD-Fenrir": {"name": "🌟 British (Fenrir) - Deep Narrator", "gender": "MALE", "type": "chirp3"},
    "en-GB-Chirp3-HD-Aoede": {"name": "🌟 British (Aoede) - Warm Female", "gender": "FEMALE", "type": "chirp3"},
    "en-US-Chirp3-HD-Charon": {"name": "🌟 American (Charon) - Ultra Natural", "gender": "NEUTRAL", "type": "chirp3"},
    
    # 📻 NEURAL2 VOICES - High quality standard voices
    "en-GB-Neural2-B": {"name": "📻 British Male (Daniel)", "gender": "MALE", "type": "neural2"},
    "en-GB-Neural2-D": {"name": "📻 British Male (James)", "gender": "MALE", "type": "neural2"},
    "en-GB-Neural2-A": {"name": "📻 British Female (Emma)", "gender": "FEMALE", "type": "neural2"},
    "en-GB-Neural2-C": {"name": "📻 British Female (Olivia)", "gender": "FEMALE", "type": "neural2"},
    "en-GB-Neural2-F": {"name": "📻 British Female (Sophie)", "gender": "FEMALE", "type": "neural2"},
    "en-US-Neural2-D": {"name": "📻 American Male (David)", "gender": "MALE", "type": "neural2"},
    "en-US-Neural2-J": {"name": "📻 American Male (John)", "gender": "MALE", "type": "neural2"},
}

class TTSService:
    def __init__(self):
        self.client = texttospeech.TextToSpeechClient()
    
    def get_available_voices(self) -> dict:
        """Return list of available voices"""
        return AVAILABLE_VOICES
    
    def synthesize(
        self,
        text: str,
        voice_name: str = "en-GB-Neural2-B",
        speaking_rate: float = 0.9,
        pitch: float = -2.0,
        audio_format: str = "MP3"
    ) -> bytes:
        """
        Synthesize text to speech using Google Cloud TTS
        
        Args:
            text: The text to synthesize
            voice_name: Voice ID (e.g., en-GB-Neural2-B)
            speaking_rate: Speed (0.25 to 4.0, default 0.9 for documentary)
            pitch: Voice pitch (-20.0 to 20.0, default -2.0 for deeper voice)
            audio_format: Output format (MP3, WAV, OGG_OPUS)
        
        Returns:
            Audio content as bytes
        """
        # Extract language code from voice name
        language_code = "-".join(voice_name.split("-")[:2])
        
        # Set up the input
        synthesis_input = texttospeech.SynthesisInput(text=text)
        
        # Configure voice
        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            name=voice_name
        )
        
        # Configure audio output
        audio_encoding_map = {
            "MP3": texttospeech.AudioEncoding.MP3,
            "WAV": texttospeech.AudioEncoding.LINEAR16,
            "OGG_OPUS": texttospeech.AudioEncoding.OGG_OPUS,
        }
        
        audio_config = texttospeech.AudioConfig(
            audio_encoding=audio_encoding_map.get(audio_format, texttospeech.AudioEncoding.MP3),
            speaking_rate=max(0.25, min(4.0, speaking_rate)),
            pitch=max(-20.0, min(20.0, pitch))
        )
        
        # Perform the synthesis
        response = self.client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )
        
        return response.audio_content


# Singleton instance
tts_service = TTSService()
