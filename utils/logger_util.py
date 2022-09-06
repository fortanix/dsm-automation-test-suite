#!/usr/bin/env python3
"""
Logger utility
"""
# -*- coding: utf-8 -*-

import logging
import os
import shutil

import sys
from datetime import datetime


def get_logger(
    name=None,
    log_level="info",
    log_filename=f"testSuite-{datetime.now().strftime('%d%m%Y%H%M%S')}.log",
    line_format="%(asctime)s [%(levelname)s %(module)s:%(lineno)d] %(message)s",
):
    _logger = logging.getLogger(name or __name__)
    _logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(fmt=line_format)

    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_handler.setLevel(log_level.upper())
    console_handler.setFormatter(formatter)
    _logger.addHandler(console_handler)

    download_dir = os.path.dirname(os.path.realpath(__file__)) + "/../reports"
    if not os.path.exists(download_dir):
        os.mkdir(download_dir)
    log_file = download_dir + "/" + log_filename
    logfile_handler = logging.FileHandler(log_file)
    logfile_handler.setLevel(log_level.upper())
    logfile_handler.setFormatter(formatter)
    _logger.addHandler(logfile_handler)
    return _logger


def main():
    _logger = get_logger(__name__)
    _logger.debug("debug message")
    _logger.info("info message")
    _logger.warning("warning message")
    _logger.error("error message")
    _logger.critical("critical message")


if __name__ == "__main__":
    sys.exit(main())
