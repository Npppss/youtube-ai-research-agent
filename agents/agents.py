from crewai import Agent
from CrewAI.tools import YouTubeTranscriptWhisperTool

transcript_tool = YouTubeTranscriptWhisperTool()

research_agent = Agent(
    role='YouTube Content Researcher',

    goal=(
        'Analyze YouTube video transcripts (from API or Whisper) and extract structured insights.'
    ),

    backstory=(
        'You are an expert research analyst specializing in extracting deep insights '
        'from video transcripts, whether from subtitles or AI-generated transcription.'
    ),

    tools=[transcript_tool],

    verbose=True,
    memory=True,
    allow_delegation=False
)