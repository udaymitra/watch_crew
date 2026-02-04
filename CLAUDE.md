# CLAUDE.md

## Project Overview

AI-powered watch price comparison system built with CrewAI. It searches multiple watch marketplaces (Chrono24, Jomashop), finds cheapest new and used listings, runs comparative price analysis, and generates buying recommendation reports.

## Tech Stack

- **Python 3.10-3.12** with **CrewAI** for multi-agent orchestration
- **Pydantic** for structured output validation
- **uv** for dependency management
- **hatchling** as build backend

## Project Structure

```
src/watch_crew/
  main.py          # Entry point — defines inputs, runs crew
  crew.py          # WatchCrew class with @agent, @task, @crew decorators
  models.py        # Pydantic models for structured task outputs
  config/
    agents.yaml    # 3 agent definitions (role, goal, backstory)
    tasks.yaml     # 4 task definitions (sequential pipeline)
  tools/           # Reserved for custom CrewAI tools (none currently)
output/            # Generated JSON + Markdown results
```

## Common Commands

```bash
# Install dependencies
crewai install
# or: uv sync

# Run the crew
crewai run
# or: python3 src/watch_crew/main.py
# or: run_crew
```

## Environment Variables

Required in `.env`:
- `MODEL` — LLM model name (e.g., `o1`)
- `OPENAI_API_KEY` — OpenAI API key
- `SERPER_API_KEY` — Serper API key for web search

## Architecture

- **Sequential pipeline**: Chrono24 search → Jomashop search → price analysis → report generation
- **3 agents**: chrono24_scraper, jomashop_scraper, watch_analyst
- **4 tasks**: search_chrono24_task, search_jomashop_task, analyze_prices_task, generate_report_task
- **Agents and tasks** are defined declaratively in YAML config files and wired via decorators in `crew.py`
- **Structured outputs**: search tasks produce `WatchSearchResults` JSON, analysis produces `WatchPriceAnalysis` JSON, report produces Markdown
- **Tools used**: SerperDevTool (Google search), ScrapeWebsiteTool, SeleniumScrapingTool — all from `crewai_tools`

## Code Conventions

- Snake_case for files and functions, PascalCase for classes
- Agent/task config lives in YAML, not Python
- Pydantic `BaseModel` subclasses for all structured outputs
- Output files go in `output/` (JSON for data, Markdown for human-readable reports)

## Key Files

- `src/watch_crew/crew.py` — core orchestration logic; start here to understand the system
- `src/watch_crew/models.py` — all data models (5 models: WatchListing, WatchSearchResults, PriceStats, ListingRecommendation, WatchPriceAnalysis)
- `src/watch_crew/main.py` — entry point with hardcoded inputs (watch query, zip code)

## Notes

- No test suite exists
- No CI/CD pipeline
- No Docker setup — runs as a standalone CLI tool
- Watch query and zip code are currently hardcoded in `main.py`
- Extensible: adding a new seller = 1 new agent in agents.yaml + 1 new task in tasks.yaml + add to analyst context
