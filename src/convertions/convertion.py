from abc import ABC, abstractmethod


class Convertion(ABC):

    @abstractmethod
    def canConvert(self, heading):
        raise NotImplementedError

    @abstractmethod
    def convert(self, heading, csv_reading):
        raise NotImplementedError
