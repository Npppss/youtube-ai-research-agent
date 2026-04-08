from crewai import Crew
from CrewAI.tasks.tasks import research_task, write_task
from CrewAI.agents.agents import research_agent, writer_agent

crew = Crew(
    agents=[research_agent, writer_agent],
    tasks=[research_task, write_task],
    verbose=True
)