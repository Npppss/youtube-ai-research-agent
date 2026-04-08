import asyncio
import yt_dlp
import whisper
from youtube_transcript_api import YouTubeTranscriptApi

# GET TRANSCRIPT (FAST)
async def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([t["text"] for t in transcript])
        return text
    except:
        return None

#DOWNLOAD AUDIO (ASYNC)
async def download_audio(video_url, output="audio.mp3"):
    loop = asyncio.get_event_loop()

    def _download():
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output,
            'quiet': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

    await loop.run_in_executor(None, _download)
    return output

#WHISPER TRANSCRIPTION (ASYNC)
async def transcribe_audio(audio_path):
    loop = asyncio.get_event_loop()

    def _transcribe():
        model = whisper.load_model("base")
        result = model.transcribe(audio_path)
        return result["text"]

    return await loop.run_in_executor(None, _transcribe)

#MAIN PIPELINE
async def process_youtube(video_url, video_id):
    transcript = await get_transcript(video_id)

    if transcript:
        print("Using YouTube Transcript")
        return transcript

    print("No transcript → using Whisper")

    audio_path = await download_audio(video_url)
    text = await transcribe_audio(audio_path)

    return text