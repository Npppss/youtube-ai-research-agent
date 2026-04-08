import asyncio
from crewai import Agent, Task, Crew
from utils.youtube_pipeline import process_youtube
# AGENT
video_researcher = Agent(
    role="Senior YouTube Researcher",
    goal="Extract deep structured insights from video transcript",
    backstory="Expert in analyzing transcripts and extracting key insights.",
    verbose=True,
)

# ASYNC WRAPPER
async def run_pipeline(video_url, video_id):
    transcript = await process_youtube(video_url, video_id)

    research_task = Task(
        description=f"""
        Analyze the following transcript and extract insights:

        {transcript}

        Requirements:
        - Minimum 5 insights
        - Bullet points
        - Include timestamps if possible
        """,
        expected_output="Structured insights from the video",
        agent=video_researcher,
    )

    crew = Crew(
        agents=[video_researcher],
        tasks=[research_task],
    )

    return crew.kickoff()

#ENTRY POINT
if __name__ == "__main__":
    video_url = "https://youtube.com/watch?v=example"
    video_id = "example"

    result = asyncio.run(run_pipeline(video_url, video_id))
    print(result)