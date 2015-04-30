#!/usr/bin/env python
# -*- coding: utf-8 -*-

import optparse
from pdict import Robot

if __name__ == "__main__":
    parser = optparse.OptionParser(usage="Usage: %prog [options]")

    parser.add_option("-i", "--init", action="store_true", dest="init", help="init the robot like database")
    parser.add_option("-s", "--start", action="store_true", dest="start", help="start the robot")

    (options, args) = parser.parse_args()

    if options.init:
        robot = Robot()
        robot.create_database()
    elif options.start:
        robot = Robot()
        robot.run("door")
    else:
        parser.print_help()
