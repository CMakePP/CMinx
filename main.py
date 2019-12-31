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
    input_path = os.path.abspath(args.file)
    output_path = None
    if args.output is not None:
         output_path = os.path.abspath(args.output)
         print(f"Writing RST files to {output_path}")
    if os.path.isdir(input_path):
        #Walk dir and add cmake files to list
        for root, subdirs, filenames in os.walk(input_path):
             for file in filenames:
                  if "cmake" == file.split(".")[-1].lower():
                       files.append(os.path.join(root, file))
             if not args.recursive:
                  break
    elif os.path.isfile(input_path):
        files.append(input_path)
    else:
        print("File is a special file (socket, FIFO, device file) and is unsupported", file=sys.stderr)
        exit(1)

    for file in files:
         documenter = Documenter(file)
         output_writer = documenter.process()
         if output_path != None:
              print(f"Writing for file {file}")
              if os.path.isdir(output_path):
                   output_filename = os.path.join(output_path, ".".join(os.path.basename(file).split(".")[:-1]) + ".rst")
                   print(f"Writing RST file {output_filename}")
                   output_writer.write_to_file(output_filename)
         else:
              print(output_writer)
              print()
