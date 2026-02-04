#!/usr/bin/env python
"""Test script: run generate_report_task in isolation with pre-collected data."""
import json
import warnings
from crewai import Agent, Crew, Process, Task

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

SITES = [
    {'key': 'chrono24', 'name': 'Chrono24'},
    {'key': 'jomashop', 'name': 'Jomashop'},
]


def main():
    with open('tests/test_input_combined.json') as f:
        search_data = json.load(f)

    with open('output/watch_price_analysis.json') as f:
        analysis_data = json.load(f)

    data_sections = "\n\n".join(
        f"--- {s['name']} Search Results ---\n{json.dumps(search_data[s['key']], indent=2)}"
        for s in SITES if s['key'] in search_data
    )
    listing_sections = "\n\n".join(
        f"## {s['name']} Listings\n"
        f"- Table of cheapest new listings (price, shipping, total, seller, link)\n"
        f"- Table of cheapest used listings"
        for s in SITES if s['key'] in search_data
    )
    analysis_json = json.dumps(analysis_data, indent=2)

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
        description=f"""Create a comprehensive markdown report for "H70405730" combining
search results and pricing analysis. Format in markdown without code blocks.

{data_sections}

--- Price Analysis ---
{analysis_json}

Sections:
## Search Summary
- Watch searched, date, sites checked, total listings found

{listing_sections}

## Cross-Site Price Comparison
- Side-by-side price stats across all sites
- New vs used premium on each site
- Which site offers better deals

## Recommendations
- Best new listing with reasoning
- Best used listing with reasoning
- Best overall deal
- New vs used recommendation""",
        expected_output=(
            "A markdown report with tables comparing watch prices across all "
            "searched sites, with clear buying recommendations."
        ),
        agent=analyst,
        output_file='output/watch_report.md',
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

    print("\n--- Report written to output/watch_report.md ---")


if __name__ == "__main__":
    main()
