#!/usr/bin/env python3

import os
import piexif
import datetime as dt
from abc import ABC, abstractclassmethod
from PIL import Image, ExifTags
from exceptions import NoMetaDataForRequestedDevice


class ReplacementData:
    _time = dt.datetime.now().strftime("%Y:%m:%d %H:%M:%S").encode("utf-8")
    _available_devices = ("samsung_s20fe",)
    SAMSUNG_S20FE = {'0th': {256: 4032, 257: 3024, 271: b'samsung', 272: b'SM-G780G', 274: 1, 282: (72, 1), 283: (72, 1), 296: 2, 305: b'G780GXXS3EWB5', 306: _time, 531: 1, 34665: 226}, 'Exif': {33434: (1, 100), 33437: (180, 100), 34850: 2, 34855: 125, 36864: b'0220', 36867: _time, 36868: _time, 36880: b'+03:00', 36881: b'+03:00', 37377: (1, 100), 37378: (169, 100), 37379: (316, 100), 37380: (0, 100), 37381: (169, 100), 37383: 2, 37385: 0, 37386: (540, 100), 37520: b'033', 37521: b'033', 37522: b'033', 40961: 1, 40962: 4032, 40963: 3024, 41986: 0, 41987: 0, 41988: (100, 100), 41989: 26, 41990: 0, 42016: b'X12QSND00YM'}, 'GPS': {}, 'Interop': {}, '1st': {256: 512, 257: 384, 259: 6, 282: (72, 1), 283: (72, 1), 296: 2, 513: 838, 514: 53876}}
  
    @classmethod
    def get(cls, device: str) -> dict:
        if not device in cls._available_devices:
            raise NoMetaDataForRequestedDevice(f"No replacement metadata fount for {device}.\n\
                Available devices -> \n{cls._available_devices}")
        data = {}
        if device == "samsung_s20fe":
            data = cls.SAMSUNG_S20FE
        return data  


class MetadataOperations(ABC):
        
    @abstractclassmethod
    def show(self):
        ...
    
    @abstractclassmethod
    def remove(self):
        ...
        
    @abstractclassmethod
    def replace(self):
        ...
    
    
class Base(MetadataOperations):
    
    def __init__(self, file_path: str="") -> None:
        self._file_path = file_path
    
    def _get_file_name(self) -> str:
        return os.path.basename(self._file_path)
    
    def _get_file_directory(self) -> str:
        return os.path.dirname(self._file_path)

    def _new_file(self, prefix: str="new_") -> str:
        new_image_name = prefix + self._get_file_name()
        directory = self._get_file_directory()
        new_file = directory + os.sep + new_image_name
        return new_file
     
    def show(self):
        ...
    
    def remove(self):
        ...
        
    def replace(self, device):
        ... 
        

class JPG(Base):
    
    def _print_metadata(self, exif_data: dict) -> dict:
        data_dict = {}
        # Loading all file's metadata to the exif_data. Available Tags:
        # IDF -----> 0th
        # IDF -----> Exif
        # IDF -----> GPS
        # IDF -----> Interop
        # IDF -----> 1st
        # IDF -----> thumbnail - image in the small resolution, also included in metadata.
        for ifd in exif_data:
                if not ifd == "thumbnail":
                    if exif_data[ifd]:
                        data_dict[ifd] = {}
                    for tag in exif_data[ifd]:
                        tag_name = piexif.TAGS[ifd][tag]["name"]
                        tag_value = exif_data[ifd][tag]
                        data_dict[ifd][tag] = tag_value
                        print(f"{ifd} --> {tag_name}: {tag_value}")
        if not data_dict:
            print("No Metadata Found.")
        # print(data_dict)
        return data_dict
            
    def _get_exif_data(self, file_path: (str | None) = None) -> dict:
        if file_path is None:
            file_path = self._file_path
        exif_data = piexif.load(file_path)
        return exif_data

    def _remove_metadata(self, new_file: str) -> None:
        image = Image.open(self._file_path)
        image_without_metadata = Image.new(image.mode, image.size)
        image_without_metadata.putdata(list(image.getdata()))
        image_without_metadata.save(new_file)
    
    def _update_metadata(self, new_file: str, new_metadata: dict) -> None:
        exif_data = self._get_exif_data(new_file)
        print("Replacing metadata .. .. ..")
        exif_data.update(new_metadata)
        exif_bytes = piexif.dump(exif_data)
        piexif.insert(exif_bytes, new_file)
            
    def _get_new_metadata(self, device: str) -> dict:
        new_data = ReplacementData.get(device)
        return new_data

    def show(self) -> (dict | None):
        try:
            exif_data = self._get_exif_data()
            return self._print_metadata(exif_data)
        except piexif._exceptions.InvalidImageDataError:
            print("Error -> Invalid Image Data")
    
    def remove(self) -> str:
        print("Removing metadata .. .. .. ")
        new_file = self._new_file()
        try:
            self._remove_metadata(new_file)
            print(f"Metadata has been removed. File saved as {new_file}")
        except Exception as ex:
            print(f"Unable to open image due to -> {ex}")
        return new_file
  
    def replace(self, device: str) -> None:
        new_metadata = self._get_new_metadata(device)
        new_file = self.remove()
        try:
            self._update_metadata(new_file, new_metadata)
            print(f"Metadata has been replaced. File saved as {new_file}")
        except piexif._exceptions.InvalidImageDataError:
            print("Error: Invalid image data")
            
    
class PNG(Base):
    def show(self) -> (dict | None):
       ...