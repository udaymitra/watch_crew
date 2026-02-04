#!/usr/bin/env python
import warnings
from watch_crew.crew import WatchCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """Run the watch price comparison crew."""
    sites = WatchCrew()._load_sites_config()

    sites_searched = ", ".join(s['name'] for s in sites)
    site_listing_sections = "\n\n".join(
        f"## {s['name']} Listings\n"
        f"- Table of cheapest new listings (price, shipping, total, seller, link)\n"
        f"- Table of cheapest used listings"
        for s in sites
    )

    inputs = {
        'watch_query': 'Rolex Submariner',
        'zip_code': '95051',
        'max_results': '10',
        'top_n': '5',
        'sites_searched': sites_searched,
        'site_listing_sections': site_listing_sections,
    }
    WatchCrew().crew().kickoff(inputs=inputs)


if __name__ == "__main__":
    run()
