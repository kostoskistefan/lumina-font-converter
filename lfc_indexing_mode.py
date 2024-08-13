from enum import Enum

class IndexingMode(Enum):
    ASCII = 1
    Unicode = 2

    def __str__(self):
        return 'ASCII' if self == IndexingMode.ASCII else 'UNICODE'
