from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, WebsiteSearchTool
from dotenv import load_dotenv
import os

load_dotenv()
from typing import List
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Blogpost():
    """Blogpost crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def market_news_monitor_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['market_news_monitor_agent'], # type: ignore[index]
            tools=[
                SerperDevTool(api_key=os.environ.get("SERPER_API_KEY")),
                ScrapeWebsiteTool(),
            ],
            verbose=True
        )

    @agent
    def data_analyst_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['data_analyst_agent'], # type: ignore[index]
            tools=[
                SerperDevTool(api_key=os.environ.get("SERPER_API_KEY")),
                WebsiteSearchTool(),
            ],
            verbose=True
        )
    @agent
    def content_creator_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['content_creator_agent'], # type: ignore[index]
            tools=[
                SerperDevTool(api_key=os.environ.get("SERPER_API_KEY")),
                WebsiteSearchTool(),
            ],
            verbose=True
        )
    @agent
    def quality_assurance_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['quality_assurance_agent'], # type: ignore[index]
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def monitor_financial_news(self) -> Task:
        return Task(
            config=self.tasks_config['monitor_financial_news'],
            agent=self.market_news_monitor_agent() # type: ignore[index]
        )

    @task
    def analyze_market_data(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_market_data'],
            agent=self.data_analyst_agent() # type: ignore[index]
        )
    @task
    def create_content(self) -> Task:
        return Task(
            config=self.tasks_config['create_content'],
            agent=self.content_creator_agent(),  # type: ignore[index]
            context=[self.monitor_financial_news(), 
            self.analyze_market_data()] # type: ignore[index]
        )
    @task
    def quality_assurance(self) -> Task:
        return Task(
            config=self.tasks_config['quality_assurance'],
            agent=self.quality_assurance_agent(),
            output_file='report.md'
            # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Blogpost crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
