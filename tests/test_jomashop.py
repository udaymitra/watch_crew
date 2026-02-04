#!/usr/bin/env python
"""Test script: run search_jomashop_task in isolation."""
import warnings
from crewai import Crew, Process
from watch_crew.crew import WatchCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def main():
    wc = WatchCrew()
    agent = wc.jomashop_scraper()
    task = wc.search_jomashop_task()

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

    # Write raw pydantic output to a Python file
    with open('output/jomashop_test_result.py', 'w') as f:
        f.write(f"# Auto-generated from test_jomashop.py\n")
        f.write(f"# Query: H70405730\n\n")
        f.write(f"raw_output = '''{result.raw}'''\n\n")
        if result.pydantic:
            f.write(f"pydantic_dict = {result.pydantic.model_dump()}\n")
        else:
            f.write(f"pydantic_dict = None  # No structured output parsed\n")

    print("\n--- Result written to output/jomashop_test_result.py ---")


if __name__ == "__main__":
    main()
