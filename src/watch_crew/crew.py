import yaml
from pathlib import Path
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from watch_crew.models import WatchSearchResults, WatchPriceAnalysis


@CrewBase
class WatchCrew():
    """WatchCrew for multi-seller watch price comparison"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def _load_sites_config(self):
        """Load site definitions from sites.yaml."""
        path = Path(__file__).parent / 'config' / 'sites.yaml'
        with open(path) as f:
            return yaml.safe_load(f)['sites']

    def _make_scraper_agent(self, site, tools):
        """Create a scraper agent for a given site, parameterized from YAML."""
        raw = self.agents_config['site_scraper']
        config = {k: v.format(**site) for k, v in raw.items()}
        return Agent(
            config=config,
            verbose=True,
            tools=tools,
        )

    def _make_search_task(self, site, agent):
        """Create an async search task for a given site, parameterized from YAML."""
        raw = self.tasks_config['search_site_task']
        return Task(
            description=raw['description'].format(**site),
            expected_output=raw['expected_output'].format(**site),
            agent=agent,
            output_file=f"output/{site['key']}_results.json",
            output_pydantic=WatchSearchResults,
            async_execution=False,
        )

    @agent
    def watch_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['watch_analyst'],
            verbose=True,
        )

    @task
    def analyze_prices_task(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_prices_task'],
            output_file='output/watch_price_analysis.json',
            output_pydantic=WatchPriceAnalysis,
        )

    @task
    def generate_report_task(self) -> Task:
        return Task(
            config=self.tasks_config['generate_report_task'],
            output_file='output/watch_report.md',
        )

    @crew
    def crew(self) -> Crew:
        sites = self._load_sites_config()
        tools = [SerperDevTool(), ScrapeWebsiteTool()]

        # Dynamic scraper agents + async search tasks
        scraper_agents = []
        search_tasks = []
        for site in sites:
            scraper = self._make_scraper_agent(site, tools)
            search_task = self._make_search_task(site, scraper)
            scraper_agents.append(scraper)
            search_tasks.append(search_task)

        # Static analyst agent + tasks from YAML
        analyst = self.watch_analyst()
        analyze = self.analyze_prices_task()
        report = self.generate_report_task()

        # Interpolate site vars so crew is self-contained (no external inputs needed)
        sites_searched = ", ".join(s['name'] for s in sites)
        site_listing_sections = "\n\n".join(
            f"## {s['name']} Listings\n"
            f"- Table of cheapest new listings (price, shipping, total, seller, link)\n"
            f"- Table of cheapest used listings"
            for s in sites
        )
        analyze.description = analyze.description.replace('{sites_searched}', sites_searched)
        report.description = report.description.replace('{site_listing_sections}', site_listing_sections)

        # Wire search results as context for downstream tasks
        analyze.context = search_tasks
        report.context = [analyze] + search_tasks

        return Crew(
            agents=scraper_agents + [analyst],
            tasks=search_tasks + [analyze, report],
            verbose=True,
            process=Process.sequential,
        )
