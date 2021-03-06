# -*- coding: utf-8 -*-

import argparse
import os
import sys
import rawdisk
import logging.config
import yaml
from . import scheme


def setup_logging(config_path=None, log_level=logging.INFO):
    """Setup logging configuration
    """

    config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format':
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': log_level,
                'formatter': 'standard',
                'stream': 'ext://sys.stdout'
            },
        },
        'loggers': {
            '': {
                'handlers': ['console'],
                'level': log_level,
                'propagate': True
            },
            'yapsy': {
                'handlers': ['console'],
                'level': logging.INFO
            }
        }
    }

    if config_path:
        if os.path.exists(config_path):
            with open(config_path, 'rt') as f:
                config = yaml.safe_load(f.read())
        else:
            print('Specified path does not exist: {}, '
                  'using default config'.format(config_path))

    logging.config.dictConfig(config)


def parse_args():
    parser = argparse.ArgumentParser(
        usage='Usage: %s -f <source>' %
              os.path.basename(sys.argv[0])
    )

    parser.add_argument(
        "--verbose", help="increase output verbosity", action="store_true")

    parser.add_argument(
        '-f', '--file', dest='filename', help='specify source file',
    )

    parser.add_argument(
        '--log-config', dest='log_config',
        help='path to YAML logging configuration file'
    )

    parser.add_argument(
        '--log-level', dest='log_level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    )

    args = parser.parse_args()

    if args.filename is None:
        parser.print_help()
        return None

    return args


def main():
    args = parse_args()

    if args is None:
        return

    logging_options = {}

    if args.log_config:
        logging_options['config_path'] = args.log_config

    if args.verbose:
        logging_options['log_level'] = logging.DEBUG
    elif args.log_level:
        logging_options['log_level'] = logging.getLevelName(args.log_level)

    setup_logging(**logging_options)
    logger = logging.getLogger(__name__)

    r = rawdisk.reader.Reader()

    try:
        r.load(args.filename)
    except IOError:
        logger.error(
            'Failed to open disk image file: {}'.format(args.filename))

    if r.scheme == scheme.common.SCHEME_MBR:
        print("Scheme: MBR")
    elif r.scheme == scheme.common.SCHEME_GPT:
        print("Scheme: GPT")
    else:
        print("Scheme: Unknown")

    print("Partitions:")
    r.list_partitions()


if __name__ == '__main__':
    main()
