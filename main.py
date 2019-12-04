#!/usr/bin/python3

from cmakedoc import documenter
import sys
documenter.Documenter(sys.argv[1:], "")
