#!/usr/bin/env python3

from creator import Creator
from arg_parser import parse
from metadata_operations import Base


def _get_args() -> tuple:
    args = parse()
    format = args.format
    path = args.path 
    command = args.command
    device = args.device
    return format, path, command, device


def _create_file_object(format: str, path: str) -> Base:
    creator = Creator(format, path)
    file = creator.instantiate()
    return file


def _actions(file: Base, command: str, device: (str | None)) -> None:
    # if command == "show":
    #     file.show()
    # if command == "remove":
    #     file.remove()
    # if command == "replace":
    #     file.replace(device)
    match command:
        case "show":
            file.show()
        case "remove":
            file.remove()
        case "replace":
            file.replace(device)


def main():
    format, path, command, device = _get_args()
    file = _create_file_object(format, path)
    _actions(file, command, device)
    

if __name__ == "__main__":
    main()
    
    

