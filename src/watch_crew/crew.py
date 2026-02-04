from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, SeleniumScrapingTool
from watch_crew.models import WatchSearchResults, WatchPriceAnalysis


@CrewBase
class WatchCrew():
    """WatchCrew for multi-seller watch price comparison"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def chrono24_scraper(self) -> Agent:
        return Agent(
            config=self.agents_config['chrono24_scraper'],
            verbose=True,
            llm=LLM("o1"),
            tools=[SerperDevTool(), ScrapeWebsiteTool(), SeleniumScrapingTool()]
        )

    @agent
    def jomashop_scraper(self) -> Agent:
        return Agent(
            config=self.agents_config['jomashop_scraper'],
            verbose=True,
            llm=LLM("o1"),
            tools=[SerperDevTool(), ScrapeWebsiteTool(), SeleniumScrapingTool()]
        )

    @agent
    def watch_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['watch_analyst'],
            verbose=True,
            llm=LLM("o1")
        )

    @task
    def search_chrono24_task(self) -> Task:
        return Task(
            config=self.tasks_config['search_chrono24_task'],
            output_file='output/chrono24_results.json',
            output_pydantic=WatchSearchResults
        )

    @task
    def search_jomashop_task(self) -> Task:
        return Task(
            config=self.tasks_config['search_jomashop_task'],
            output_file='output/jomashop_results.json',
            output_pydantic=WatchSearchResults
        )

    @task
    def analyze_prices_task(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_prices_task'],
            output_file='output/watch_price_analysis.json',
            output_pydantic=WatchPriceAnalysis
        )

    @task
    def generate_report_task(self) -> Task:
        return Task(
            config=self.tasks_config['generate_report_task'],
            output_file='output/watch_report.md'
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=True,
            process=Process.sequential
        )
