#!/usr/bin/python3

from cmakedoc.documenter import Documenter
import sys

if __name__ == "__main__":
    documenter = Documenter(sys.argv[1:], "")
    documenter.process()
