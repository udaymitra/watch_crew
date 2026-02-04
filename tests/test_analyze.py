#!/usr/bin/env python
"""Test script: run analyze_prices_task in isolation with pre-collected search data."""
import json
import warnings
from crewai import Agent, Crew, Process, Task
from watch_crew.models import WatchPriceAnalysis

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

SITES = [
    {'key': 'chrono24', 'name': 'Chrono24'},
    {'key': 'jomashop', 'name': 'Jomashop'},
]


def main():
    with open('tests/test_input_combined.json') as f:
        data = json.load(f)

    data_sections = "\n\n".join(
        f"--- {s['name']} Search Results ---\n{json.dumps(data[s['key']], indent=2)}"
        for s in SITES if s['key'] in data
    )
    sites_searched = ", ".join(s['name'] for s in SITES if s['key'] in data)

    analyst = Agent(
        role="Watch Market Pricing Analyst",
        goal="Analyze watch pricing data across multiple sellers to provide buying recommendations",
        backstory=(
            "You are a seasoned watch market analyst who specializes in pricing "
            "trends and value assessment across multiple marketplaces."
        ),
        verbose=True,
    )

    task = Task(
        description=f"""Analyze the watch search results from all searched sites for
"H70405730" and provide comprehensive pricing insights.

Sites searched: {sites_searched}

{data_sections}

Analysis steps:
1. Price statistics per site per condition (min, max, median, average)
2. Cross-site comparison: which seller is cheaper for new? For used?
3. New vs used premium percentage on each site
4. Factor in shipping costs for true total cost comparison
5. Identify the single best new listing across all sites
6. Identify the single best used listing across all sites
7. Identify the overall best deal regardless of condition
8. Flag any pricing anomalies (suspiciously low, much higher than peers)
9. Provide a clear new vs used recommendation with reasoning""",
        expected_output=(
            "Structured JSON matching the WatchPriceAnalysis model with complete "
            "pricing statistics per site, recommendations, and market observations."
        ),
        agent=analyst,
        output_file='output/watch_price_analysis.json',
        output_pydantic=WatchPriceAnalysis,
    )

    crew = Crew(
        agents=[analyst],
        tasks=[task],
        verbose=True,
        process=Process.sequential,
    )

    result = crew.kickoff(inputs={
        'watch_query': 'H70405730',
    })

    with open('output/analyze_test_result.py', 'w') as f:
        f.write("# Auto-generated from test_analyze.py\n")
        f.write("# Query: H70405730\n\n")
        f.write(f"raw_output = '''{result.raw}'''\n\n")
        if result.pydantic:
            f.write(f"pydantic_dict = {result.pydantic.model_dump()}\n")
        else:
            f.write("pydantic_dict = None  # No structured output parsed\n")

    print("\n--- Result written to output/analyze_test_result.py ---")


if __name__ == "__main__":
    main()
