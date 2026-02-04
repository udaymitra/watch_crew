# Watch Price Comparison with CrewAI

An AI-powered tool that compares watch prices across multiple sellers (Chrono24, Jomashop), finds the cheapest new and used listings, and provides data-driven buying recommendations. Built with [CrewAI](https://crewai.com).

## What It Does

1. **Chrono24 Search**: Scrapes Chrono24 for new and pre-owned watch listings
2. **Jomashop Search**: Scrapes Jomashop for new and pre-owned watch listings
3. **Price Analysis**: Compares prices across sellers with statistics and anomaly detection
4. **Report Generation**: Produces a markdown report with tables and buying recommendations

## Installation

1. Clone the repository and install dependencies:

    ```bash
    cd watch_crew
    crewai install
    ```

## Environment Setup

1. Add your API keys to `.env`:
    - Required:
        - `OPENAI_API_KEY`: OpenAI API key
        - `SERPER_API_KEY`: Serper API key for web search
    - Optional:
        - `MODEL`: LLM model name (defaults to `o1`)

## Quick Start

1. Edit the search parameters in `src/watch_crew/main.py`:
    - `watch_query`: Watch model to search (e.g., `'Rolex Submariner'`)
    - `zip_code`: US zip code for shipping estimates (e.g., `'95051'`)
    - `max_results`: Max listings to collect per site (e.g., `'10'`)
    - `top_n`: Top cheapest to return per category (e.g., `'5'`)

2. Run the comparison crew:
    ```bash
    crewai run
    ```

## Output Files

The tool generates four files in the `output/` directory:

- `chrono24_results.json`: Cheapest new and used listings from Chrono24
- `jomashop_results.json`: Cheapest new and used listings from Jomashop
- `watch_price_analysis.json`: Cross-site pricing statistics and recommendations
- `watch_report.md`: Human-readable markdown report with tables

## Architecture

The system uses three specialized AI agents in a sequential pipeline:

1. **Chrono24 Scraper**: Searches Chrono24 for watch listings using Google search and web scraping
2. **Jomashop Scraper**: Searches Jomashop for watch listings using Google search and web scraping
3. **Watch Analyst**: Analyzes pricing data across both sellers and generates recommendations

## Requirements

- Python `>= 3.10` and `< 3.13`
- OpenAI API key
- Serper API key

## Support

- [CrewAI Documentation](https://docs.crewai.com)
- [Community Forum](https://community.crewai.com)
