#!/usr/bin/env python3

from abc import ABC, abstractmethod


class Database(ABC):
    @abstractmethod
    def query(self):
        raise NotImplementedError

    @abstractmethod
    def display(self):
        raise NotImplementedError

    @abstractmethod
    def add(self):
        raise NotImplementedError

    @abstractmethod
    def delete(self):
        raise NotImplementedError

    @abstractmethod
    def edit(self):
        raise NotImplementedError
