#!/usr/bin/python3

from cmakedoc.documenter import Documenter
import sys
import argparse
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="CMake file to generate documentation for. If directory, will generate documentation for all .cmake files")
    parser.add_argument("-o", "--output", help="Directory to output generated RST to. If not specified will print to standard output. Output files will have the original filename with the cmake extension replaced by .rst")
    parser.add_argument("-r", "--recursive", help="If specified, will generate documentation for all subdirectories of specified directory recursively", action="store_true")
    args = parser.parse_args()
    files = []
    if os.path.isdir(args.file):
        #Walk dir and add cmake files to list
        for root, subdirs, filenames in os.walk(args.file):
             for file in filenames:
                  if "cmake" == file.split(".")[-1].lower():
                       files.append(os.path.join(root, file))
             if not args.recursive:
                  break
    elif os.path.isfile(args.file):
        files.append(args.file)
    else:
        print("File is a special file (socket, FIFO, device file) and is unsupported", file=sys.stderr)
        exit(1)

    documenter = Documenter(files, args.output)
    documenter.process()

