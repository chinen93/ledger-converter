from abc import ABC, abstractmethod


class Convertion(ABC):

    @staticmethod
    @abstractmethod
    def canConvert(heading):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def convert(heading, csv_reading):
        raise NotImplementedError
