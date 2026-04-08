from crewai_tools import BaseTool
from youtube_transcript_api import YouTubeTranscriptApi
import whisper
import yt_dlp
import os
import re

class YouTubeTranscriptWhisperTool(BaseTool):
    name: str = "YouTube Transcript + Whisper Tool"
    description: str = "Fetch transcript or generate transcript using Whisper"

    def _extract_video_id(self, url: str) -> str:
        match = re.search(r"v=([^&]+)", url)
        return match.group(1)

    def _download_audio(self, url: str, filename="audio.mp3"):
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': filename,
            'quiet': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return filename

    def _run(self, youtube_video_url: str) -> str:
        try:
            # 1. Try Transcript API
            video_id = self._extract_video_id(youtube_video_url)
            transcript = YouTubeTranscriptApi.get_transcript(video_id)

            full_text = " ".join([t["text"] for t in transcript])
            return f"[Transcript API]\n{full_text[:5000]}"

        except Exception:
            try:
                # 2. Fallback to Whisper

                audio_file = self._download_audio(youtube_video_url)

                model = whisper.load_model("base")  # bisa diganti small/medium
                result = model.transcribe(audio_file)

                os.remove(audio_file)

                return f"[Whisper]\n{result['text'][:5000]}"

            except Exception as e:
                return f"Error processing video: {str(e)}"