#!/usr/bin/env python3

import os
import piexif
import datetime as dt
from abc import ABC, abstractclassmethod
from PIL import Image, ExifTags
from exceptions import NoMetaDataForRequestedDevice, DoesNotApplicableForCurrentFormat


class ReplacementData:
    _time = dt.datetime.now().strftime("%Y:%m:%d %H:%M:%S").encode("utf-8")
    available_options = ("samsung_s20fe", "iphone_6s")
    
    SAMSUNG_S20FE = {'0th': {256: 4032, 257: 3024, 271: b'samsung', 272: b'SM-G780G', 274: 1, 282: (72, 1), 283: (72, 1), 296: 2, 305: b'G780GXXS3EWB5', 306: _time, 531: 1, 34665: 226}, 'Exif': {33434: (1, 100), 33437: (180, 100), 34850: 2, 34855: 125, 36864: b'0220', 36867: _time, 36868: _time, 36880: b'+03:00', 36881: b'+03:00', 37377: (1, 100), 37378: (169, 100), 37379: (316, 100), 37380: (0, 100), 37381: (169, 100), 37383: 2, 37385: 0, 37386: (540, 100), 37520: b'033', 37521: b'033', 37522: b'033', 40961: 1, 40962: 4032, 40963: 3024, 41986: 0, 41987: 0, 41988: (100, 100), 41989: 26, 41990: 0, 42016: b'X12QSND00YM'}, 'GPS': {}, 'Interop': {}, '1st': {256: 512, 257: 384, 259: 6, 282: (72, 1), 283: (72, 1), 296: 2, 513: 838, 514: 53876}}
    IPHONE_6S = {'0th': {271: b'Apple', 272: b'iPhone 6s Plus', 274: 1, 282: (72, 1), 283: (72, 1), 296: 2, 305: b'12.4.1', 306: _time, 531: 1, 34665: 200}, 'Exif': {33434: (1, 4), 33437: (11, 5), 34850: 2, 34855: 125, 36864: b'0221', 36867: _time, 36868: _time, 37121: b'\x01\x02\x03\x00', 37377: (31507, 15753), 37378: (193685, 85136), 37379: (-51553, 44873), 37380: (0, 1), 37383: 5, 37385: 24, 37386: (83, 20), 37396: (659, 720, 310, 311), 37500: b"Apple iOS\x00\x00\x01MM\x00\x16\x00\x01\x00\t\x00\x00\x00\x01\x00\x00\x00\n\x00\x02\x00\x07\x00\x00\x02.\x00\x00\x01\x1c\x00\x03\x00\x07\x00\x00\x00h\x00\x00\x03J\x00\x04\x00\t\x00\x00\x00\x01\x00\x00\x00\x01\x00\x05\x00\t\x00\x00\x00\x01\x00\x00\x00\x82\x00\x06\x00\t\x00\x00\x00\x01\x00\x00\x00u\x00\x07\x00\t\x00\x00\x00\x01\x00\x00\x00\x01\x00\x08\x00\n\x00\x00\x00\x03\x00\x00\x03\xb2\x00\t\x00\t\x00\x00\x00\x01\x00\x00\x12\x13\x00\x0c\x00\n\x00\x00\x00\x02\x00\x00\x03\xca\x00\r\x00\t\x00\x00\x00\x01\x00\x00\x00(\x00\x0e\x00\t\x00\x00\x00\x01\x00\x00\x00\x00\x00\x0f\x00\t\x00\x00\x00\x01\x00\x00\x00\x02\x00\x10\x00\t\x00\x00\x00\x01\x00\x00\x00\x01\x00\x14\x00\t\x00\x00\x00\x01\x00\x00\x00\x05\x00\x17\x00\t\x00\x00\x00\x01\x00\x00\x00\x00\x00\x19\x00\t\x00\x00\x00\x01\x00\x00\x00\x00\x00\x1c\x00\t\x00\x00\x00\x01\x00\x00\x00\x03\x00\x1f\x00\t\x00\x00\x00\x01\x00\x00\x00\x00\x00%\x00\t\x00\x00\x00\x01\x00\x00\x00\x00\x00&\x00\t\x00\x00\x00\x01\x00\x00\x00\x00\x00'\x00\n\x00\x00\x00\x01\x00\x00\x03\xda\x00\x00\x00\x00bplist00O\x11\x02\x00\xbd\x00\x92\x00\x9d\x00\xa1\x00k\x00b\x00\\\x00X\x00V\x00f\x00\x81\x00\x99\x00\xa4\x00\xbc\x00\xc6\x00\xbe\x00\xc3\x00\x96\x00\xd5\x00\x99\x00t\x00h\x00\\\x00T\x00Z\x00X\x00L\x00E\x00A\x00;\x00:\x00J\x00\xaa\x00\x9c\x00\xd0\x00\x98\x00~\x00j\x00^\x00V\x00i\x00j\x00l\x00b\x00Y\x00A\x008\x006\x00\xac\x00\xad\x00\xd8\x00\x8d\x00\x89\x00s\x00h\x00Y\x00V\x00R\x00U\x00[\x00i\x00R\x00I\x00K\x00\xea\x00\xad\x00\xbe\x00\x83\x00z\x00m\x00`\x00V\x00p\x00z\x00b\x00E\x00F\x00E\x00F\x00?\x00\xcf\x00\xa0\x00\x94\x00\x81\x00w\x00j\x00e\x00[\x00\x8a\x00\x97\x00^\x00R\x00A\x00:\x00=\x00;\x00\xd6\x00\xb3\x00\xae\x00\x89\x00~\x00l\x00a\x00U\x00M\x00J\x00D\x00?\x00;\x007\x005\x002\x00\xdb\x00\xb1\x00\xcb\x00\x96\x00\x8b\x00}\x00j\x00\\\x00Q\x00\\\x00c\x00X\x00D\x00?\x007\x008\x00\xd2\x00\xc1\x00\xa4\x00\x9a\x00\x8f\x00r\x00h\x00Y\x00P\x00V\x00\x84\x00Y\x00E\x00:\x00<\x00E\x00\xc5\x00\xbb\x00\xae\x00\x96\x00\x9c\x00\x83\x00x\x00`\x00c\x00M\x00Z\x00`\x00M\x00<\x00:\x00B\x00\xb6\x00\x9d\x00\xa9\x00\x91\x00\x9a\x00\x87\x00w\x00`\x00\x81\x00\x80\x00r\x00k\x00y\x00J\x00H\x00H\x00\xac\x00\xa3\x00\xb1\x00\x8c\x00\x8a\x00m\x00v\x00d\x00x\x00o\x00h\x00`\x00Z\x00G\x00=\x00@\x00\x9b\x00\x8d\x00\x82\x00u\x00j\x00`\x00W\x00T\x00U\x00T\x00S\x00U\x00S\x00O\x00U\x00\x8b\x00\xef\x00\x8d\x00\x83\x00\x85\x00\x82\x00{\x00`\x00\xa4\x00\x0c\x01\xec\x00\xdd\x00\xc6\x00\xc4\x00\xc6\x00\xbf\x00\xaf\x00\xeb\x00\xb2\x00\xa6\x00\xc9\x00\x8f\x00\x90\x00t\x00\xaa\x00\xfb\x00\xee\x00\xdf\x00\xe1\x00\xca\x00\xad\x00\xb0\x00\xca\x00\xcf\x00{\x00s\x00i\x00q\x00b\x00S\x00Z\x00[\x00I\x00>\x008\x006\x005\x005\x00:\x00\x00\x08\x00\x00\x00\x00\x00\x00\x02\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x0cbplist00\xd4\x01\x02\x03\x04\x05\x06\x07\x08UflagsUvalueYtimescaleUepoch\x10\x01\x13\x00\x02\xf3\xa2v\x03\x0c)\x12;\x9a\xca\x00\x10\x00\x08\x11\x17\x1d'-/8=\x00\x00\x00\x00\x00\x00\x01\x01\x00\x00\x00\x00\x00\x00\x00\t\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00?\xff\xff\xda\x8c\x00\x02k\xc7\xff\xff]D\x00\x00\xa8\xab\xff\xff\xe0U\x00\x00\x91@\x00\x00\x00\x81\x00\x00\x01\x00\x00\x00\x007\x00\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00\x01", 37521: b'506', 37522: b'506', 40960: b'0100', 40961: 1, 40962: 4032, 40963: 3024, 41495: 2, 41729: b'\x01', 41986: 0, 41987: 0, 41989: 29, 41990: 0, 42034: ((83, 20), (83, 20), (11, 5), (11, 5)), 42035: b'Apple', 42036: b'iPhone 6s Plus back camera 4.15mm f/2.2'}, '1st': {259: 6, 282: (72, 1), 283: (72, 1), 296: 2, 513: 1860, 514: 8776}}
    
    @classmethod
    def get(cls, device: str) -> dict:
        if not device in cls.available_options:
            raise NoMetaDataForRequestedDevice(f"No replacement metadata found for {device}.\n\
                Available devices -> \n{cls.available_options}")
        data: dict = {}
        if device == "samsung_s20fe":
            data = cls.SAMSUNG_S20FE
        if device == "iphone_6s":
            data = cls.IPHONE_6S
        return data  


class MetadataOperations(ABC):
        
    @abstractclassmethod
    def show(self):
        pass
    
    @abstractclassmethod
    def remove(self):
        pass
        
    @abstractclassmethod
    def replace(self, device):
        pass
    
    
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
        raise NotImplementedError
    
    def remove(self):
        raise NotImplementedError
        
    def replace(self, device):
        raise NotImplementedError
        

class JPG(Base):
    
    def _print_metadata(self, exif_data: dict) -> None:
        data_dict: dict = {}
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
        # prints 'dict', that can be added to the ReplacementData class as a new template.
        # print(data_dict)

            
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
        print("Inserting metadata from template .. .. ..")
        exif_data.update(new_metadata)
        exif_bytes = piexif.dump(exif_data)
        piexif.insert(exif_bytes, new_file)
            
    def _get_new_metadata(self, device: str) -> dict:
        new_data = ReplacementData.get(device)
        return new_data

    def show(self) -> None:
        try:
            exif_data = self._get_exif_data()
            self._print_metadata(exif_data)
        except piexif._exceptions.InvalidImageDataError:
            print("Error -> Invalid Image Data")
            return None
    
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
    def show(self) -> None:
        ...
    
    def remove(self) -> None:
        ...
    
    def replace(self, device: str) -> None:
        raise DoesNotApplicableForCurrentFormat(f"Function '--replace' does NOT work with PNG format.")