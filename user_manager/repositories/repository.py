from abc import ABC, abstractmethod
from dataclasses import dataclass

from asyncpg import Pool


@dataclass
class IRepository(ABC):
    pool: Pool

    @abstractmethod
    def all(self):
        raise NotImplementedError

    @abstractmethod
    def get(self):
        raise NotImplementedError

    @abstractmethod
    def create(self):
        raise NotImplementedError

    @abstractmethod
    def update(self):
        raise NotImplementedError

    @abstractmethod
    def delete(self):
        raise NotImplementedError
