from CrewAI.crew import crew

result = crew.kickoff(
    inputs={
        "youtube_video_url": "https://youtube.com/watch?v=example"
    }
)

print(result)