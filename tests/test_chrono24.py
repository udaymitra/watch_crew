#!/usr/bin/env python
"""Test script: run a single site search task in isolation."""
import warnings
from crewai import Crew, Process
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from watch_crew.crew import WatchCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

SITE = {
    'key': 'chrono24',
    'name': 'Chrono24',
    'domain': 'chrono24.com',
    'description': "the world's largest online marketplace for luxury watches",
    'search_specialty': (
        'You know how to search for specific models, filter by condition '
        '(new vs pre-owned), and extract detailed listing information including '
        'prices, shipping costs, and seller details.'
    ),
}


def main():
    wc = WatchCrew()
    tools = [SerperDevTool(), ScrapeWebsiteTool()]
    agent = wc._make_scraper_agent(SITE, tools)
    task = wc._make_search_task(SITE, agent)
    task.async_execution = False

    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=True,
        process=Process.sequential,
    )

    result = crew.kickoff(inputs={
        'watch_query': 'H70405730',
        'zip_code': '95051',
        'max_results': '4',
        'top_n': '2',
    })

    with open('output/chrono24_test_result.py', 'w') as f:
        f.write("# Auto-generated from test_chrono24.py\n")
        f.write("# Query: H70405730\n\n")
        f.write(f"raw_output = '''{result.raw}'''\n\n")
        if result.pydantic:
            f.write(f"pydantic_dict = {result.pydantic.model_dump()}\n")
        else:
            f.write("pydantic_dict = None  # No structured output parsed\n")

    print("\n--- Result written to output/chrono24_test_result.py ---")


if __name__ == "__main__":
    main()
