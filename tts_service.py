"""
TTS Service - Cartesia Text-to-Speech wrapper
Chỉ sử dụng Vietnamese voices
"""
from cartesia import Cartesia
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class TTSService:
    def __init__(self):
        api_key = os.getenv("CARTESIA_API_KEY")
        if not api_key:
            raise ValueError("CARTESIA_API_KEY environment variable is required")
        self.client = Cartesia(api_key=api_key)
        self._voices_cache = None
    
    def get_available_voices(self) -> list:
        """
        Return list of available Vietnamese voices
        """
        return [
            {
                "id": "935a9060-373c-49e4-b078-f4ea6326987a",
                "name": "Linh - Vietnamese Female ⭐",
                "gender": "female",
            },
            {
                "id": "0e58d60a-2f1a-4252-81bd-3db6af45fb41",
                "name": "Minh - Vietnamese Male ⭐",
                "gender": "male",
            },
        ]
    
    def synthesize(
        self,
        text: str,
        voice_id: str,
        speaking_rate: float = 1.0,
    ) -> bytes:
        """
        Synthesize text to speech using Cartesia TTS
        
        Args:
            text: The text to synthesize
            voice_id: Voice UUID from Cartesia
            speaking_rate: Speed (-1.0 to 1.0, 0 is normal, negative is slower, positive is faster)
        
        Returns:
            Audio content as bytes (MP3 format)
        """
        # Convert speaking_rate from 0.25-4.0 range to Cartesia's -1.0 to 1.0 range
        # 1.0 (normal) -> 0, 0.5 -> -0.5, 2.0 -> 0.5
        cartesia_speed = "normal"
        if speaking_rate < 0.8:
            cartesia_speed = "slowest"
        elif speaking_rate < 0.95:
            cartesia_speed = "slow"
        elif speaking_rate > 1.3:
            cartesia_speed = "fastest"
        elif speaking_rate > 1.1:
            cartesia_speed = "fast"
        
        audio_chunks = []
        try:
            for chunk in self.client.tts.bytes(
                model_id="sonic-3",
                transcript=text,
                voice={"mode": "id", "id": voice_id},
                language="vi",
                output_format={
                    "container": "mp3",
                    "sample_rate": 44100,
                    "bit_rate": 128000,
                },
            ):
                audio_chunks.append(chunk)
        except Exception as e:
            raise Exception(f"TTS synthesis failed: {str(e)}")
        
        return b"".join(audio_chunks)


# Singleton instance
tts_service = TTSService()
