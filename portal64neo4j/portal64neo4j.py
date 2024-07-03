import logging
from pathlib import Path
import sys
from typing import List
from dotenv import dotenv_values
from neo4j import GraphDatabase

from utilities import get_parser, logging_cfg

LOGGER = logging.getLogger("portal64neo4j.py")


def main(args: List[str]) -> None:
    """ """
    parser = get_parser("Analyzing SVS Portal64 Seasons with Neo4j")
    options = parser.parse_args(args)

    logging_cfg(filename="logging.ini", loglevel=options.loglevel)
    LOGGER.info("Called with '%s'", options)

    config = dotenv_values(Path(__file__).parent / ".env", verbose=True)
    app = Portal64Neo4j(
        config["NEO4J_SERVERURL"], config["NEO4J_USER"], config["NEO4J_PASSWORD"]
    )


class Portal64Neo4j:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        LOGGER.info(
            f"{self.__class__.__name__} started driver {self.driver.__class__.__name__} "
        )

    def __del__(self):
        LOGGER.info("Closing")
        self.driver.close()
        LOGGER.info(
            f"{self.__class__.__name__} closed driver {self.driver.__class__.__name__}"
        )


def init():
    """Initialization that is executed at the time of the module import."""
    if __name__ == "__main__":
        sys.exit(main(sys.argv[1:]))


init()
