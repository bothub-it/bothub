import sys
import plac

from .tools.bothub import get_token as bothub_get_token


commands = {
    'bothub_get_token': bothub_get_token,
}

@plac.annotations(
    command=plac.Annotation(choices=commands.keys()))
def main(command, *args):
    plac.call(commands.get(command), args)

plac.call(main, sys.argv[1:])