import re
import argparse

PLATFORM = {
    'win': r'^mozilla/5.0 \(windows;',
    'linux': r'^mozilla/5.0 \(x11;.*linux',
    'mac': r'^mozilla/5.0 \(macintosh'
}


def compile_regexp_config():
    for key in PLATFORM:
        PLATFORM[key] = re.compile(PLATFORM[key], re.I)


def setup_arg_parser(parser):
    parser.add_argument('-p', '--platform')
    parser.add_argument('-i', '--inc-pattern', nargs='*', default=[])
    parser.add_argument('-x', '--exc-pattern', nargs='*', default=[])


def main(platform, inc_pattern, exc_pattern, **kwargs):
    compile_regexp_config()
    inc_pattern = [x.lower() for x in inc_pattern]
    exc_pattern = [x.lower() for x in exc_pattern]
    for line in open('var/ua_uniq.txt'):
        line = line.strip().lower()
        if platform:
            if not PLATFORM[platform].search(line):
                continue
        if inc_pattern:
            if not all(x in line for x in inc_pattern):
                continue
        if exc_pattern:
            if any(x in line for x in exc_pattern):
                continue
        print(line)
