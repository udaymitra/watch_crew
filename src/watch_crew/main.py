#!/usr/bin/env python
import warnings
from watch_crew.crew import WatchCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """Run the watch price comparison crew."""
    inputs = {
        'watch_query': 'Rolex Submariner',
        'zip_code': '95051',
        'max_results': '10',
        'top_n': '5',
    }
    WatchCrew().crew().kickoff(inputs=inputs)


if __name__ == "__main__":
    run()
