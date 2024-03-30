from openai import OpenAI
import sounddevice as sd
import soundfile as sf
from pathlib import Path
import arabic_reshaper
from bidi.algorithm import get_display




client = OpenAI(api_key="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")
speech_file_path = Path(__file__).parent / "speech.mp3"
text = "كيف حالك"
with client.audio.speech.with_streaming_response.create(
    model="tts-1",
    voice="echo",
    #input='"' + bidi_text + '"'
    input = text
) as response:
    # This doesn't seem to be *actually* streaming, it just creates the file
    # and then doesn't update it until the whole generation is finished

    response.stream_to_file(speech_file_path)
    audio_data,sample_rate = sf.read(speech_file_path)
    sd.play(audio_data,sample_rate)
    sd.wait()