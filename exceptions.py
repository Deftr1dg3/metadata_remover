#!/usr/bin/env python3

class NoDataProvided(Exception):
    ...
    
class FileFormatNotSpecified(Exception):
    ...
    
class FileFormatIsNotSupported(Exception):
    ...

class WrongInputFormat(Exception):
    ...

class NoMetaDataForRequestedDevice(Exception):
    ... 

class ArgumentRequiredError(Exception):
    ...

class DoesNotApplicableForCurrentFormat(Exception):
    ...