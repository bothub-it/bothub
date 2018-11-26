import sys
import logging
import plac

from . import logger as cli_logger
from ..services import logger as services_logger
from .tools.bothub import get_token as bothub_get_token
from .run import run


LOGGER_FORMAT = {
    'StreamHandler': '%(name)-22s - %(levelname)-8s - %(message)s',
    'FileHandler': '%(asctime)-15s - %(name)-22s - %(levelname)-8s - %(message)s'
}

commands = {
    'bothub_get_token': bothub_get_token,
    'run': run,
}

@plac.annotations(
    debug=plac.Annotation(kind='flag', abbrev='D'),
    command=plac.Annotation(choices=commands.keys()))
def main(debug, command, *args):
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG if debug else logging.INFO)
    ch.setFormatter(logging.Formatter(LOGGER_FORMAT.get('StreamHandler')))
    fh = logging.FileHandler('nlu_benchmark.log')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(LOGGER_FORMAT.get('FileHandler')))

    for logger in [cli_logger, services_logger]:
        logger.setLevel(logging.DEBUG)
        logger.addHandler(fh)
        logger.addHandler(ch)

    cli_logger.info(f'NLU Benchmark running {command} command')

    try:
        plac.call(commands.get(command), args)
    except Exception as e:
        cli_logger.exception(e)


plac.call(main, sys.argv[1:])
