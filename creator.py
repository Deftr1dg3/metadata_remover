#!/usr/bin/env python3

import os
from metadata_operations import Base, JPG, PNG

class Creator:
    def __init__(self, file_format: str, file_path: str) -> None:
        self._file_format = file_format
        self._file_path = os.getcwd() + os.sep + file_path.strip("." + os.sep)
    
    def instantiate(self) -> Base:
        instance = Base()
        if self._file_format in ["jpg", "jpeg"]:
            instance = JPG(self._file_path)
        if self._file_format == "png":
            instance = PNG(self._file_path)
        return instance
        

