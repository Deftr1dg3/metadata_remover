#!/usr/bin/env python3

import os
import argparse
from typing import NamedTuple
from metadata_operations import ReplacementData
from exceptions import NoDataProvided, FileFormatNotSpecified, FileFormatIsNotSupported, WrongInputFormat, ArgumentRequiredError

SUPPORTED_FORMATS = ("jpg", "jpeg", "png", "py")

class ParsedData(NamedTuple):
    format: str
    path: str
    command: str
    device: (str | None)
    

parser = argparse.ArgumentParser()

parser.add_argument("-s", "--show", type=str, help="Insert PATH to the file. Shows metadata of the file if it persists.\
    Otherwise shows notification, that there is no metadata in the current file.")
parser.add_argument("-r", "--remove", type=str, help="Insert PATH to the file. Removes all metadata from the file.")
parser.add_argument("--replace", action="store_true", help="Replace Metadata of the give file.")
parser.add_argument("-d", "--device", type=str, help=f"REQUIRED WITH '--replace'.\n\
    Metadate template for the specified device. Available optiond -->\n{ReplacementData.available_options}")
parser.add_argument("-p", "--path", type=str, help="REQUIRED WITH '--replace'. Path to the file.")


def _validate_device_and_path(args: argparse.Namespace) -> tuple:
    device = args.device
    path = args.path
    print(f"PATH -> {path}")
    if not device or not path:
        raise ArgumentRequiredError("Error -> '--device' and '--path' arguments are required with '--replace'.")
    return device, path
    

def _validate_path(path: str) -> bool:
    if os.path.exists(path):
        return True 
    raise FileNotFoundError(f"Expected for -> metadata --$(option) '/path/to/the/file.${SUPPORTED_FORMATS}' input. But got metadata --$(option) '{path}'")


def _get_file_format(path: str) -> str:
    path = path.lower().strip(".")
    format = path.rpartition(".")[-1]
    if path == format:
        raise FileFormatNotSpecified(f"Expected for -> metadata --$(option) '/path/to/the/file.${SUPPORTED_FORMATS}' input. But got '{path}'")
    if format not in SUPPORTED_FORMATS:
        raise FileFormatIsNotSupported(f"Expected for -> metadata --$(option) '/path/to/the/file.${SUPPORTED_FORMATS}'. But got '{path}'.")
    return format
    
    
def _validate_data(args: argparse.Namespace) -> bool:
    if any((args.show, args.remove, args.replace)):
        return True 
    raise NoDataProvided(f"Expected for -> 'metadata --$(option) '/path/to/the/file.${SUPPORTED_FORMATS}' input.")     

def _on_show(args: argparse.Namespace) -> tuple:
    path = args.show
    _validate_path(path)
    format = _get_file_format(path)
    command = "show"
    return format, path, command

def _on_remove(args: argparse.Namespace) -> tuple:
    path = args.remove
    _validate_path(path)
    format = _get_file_format(path)
    command = "remove"
    return format, path, command

def _on_replace(args: argparse.Namespace) -> tuple:
    device, path = _validate_device_and_path(args)
    format = _get_file_format(path)
    command = "replace"
    return format, path, command, device
       
def parse() -> ParsedData:
    args = parser.parse_args()
    _validate_data(args)
    format = ""
    path = ""
    command = ""
    device = None
    if args.show:
        format, path, command = _on_show(args)
    if args.remove:
        format, path, command = _on_remove(args)
    if args.replace:
        format, path, command, device = _on_replace(args)
    return ParsedData(format=format, path=path, command=command, device=device)


if __name__ == "__main__":
    print(parse())
    
