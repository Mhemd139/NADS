import time
from openai import OpenAI
import openai
import playsound
from playsound import playsound
import arabic_reshaper
from bidi.algorithm import get_display
from pathlib import Path
import sounddevice as sd
import soundfile as sf
import elevenlabs


elevenlabs.set_api_key("89cd54ea93ee501c50e939a5abda0327") 
#The Path of the Speech's File
speech_file_path = Path(__file__).parent / "speech.mp3"
# Enter your Assistant ID here.
ASSISTANT_ID = "asst_7Rv1r9reYeAP0P3pdq4invki"
# Make sure your API key is set as an environment variable.
client = OpenAI(api_key="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")
# Create a thread with a message.
thread = client.beta.threads.create(
    messages=[
        {
            "role": "user",
            # Update this with the query you want to use.
            "content": "" 
        }
    ]
)

# Submit the thread to the assistant (as a new run).
run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=ASSISTANT_ID)
print(f"👉 Run Created: {run.id}")

# Wait for run to complete.
while run.status != "completed":
    run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
    print(f"🏃 Run Status: {run.status}")
    time.sleep(1)
else:
    print(f"🏁 Run Completed!")

# Get the latest message from the thread.
message_response = client.beta.threads.messages.list(thread_id=thread.id)
messages = message_response.data

# Print the latest message.
latest_message = messages[0]
reshaped_text = arabic_reshaper.reshape(latest_message.content[0].text.value)
bidi_text = get_display(reshaped_text)
print(f"💬 Response: {bidi_text}")



#Convert the response to audio and play it
#audio = elevenlabs.generate(
#    text=latest_message.content[0].text.value,
#    voice="James" # or any voice of your choice
#)
#elevenlabs.play(audio)

with client.audio.speech.with_streaming_response.create(
    model="tts-1-hd",
    voice="onyx",
    input= latest_message.content[0].text.value
) as response:
    # This doesn't seem to be *actually* streaming, it just creates the file
    # and then doesn't update it until the whole generation is finished
    response.stream_to_file(speech_file_path)

    audio_data,sample_rate = sf.read(speech_file_path)
    sd.play(audio_data,sample_rate)
    sd.wait()


