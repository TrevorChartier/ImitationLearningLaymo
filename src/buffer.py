"""Defines a buffer that can be quickly stride indexed"""
import numpy as np

class Buffer:
    def __init__(self, len: int):
        self._buffer = np.zeros(len, dtype = np.int8)
        self._idx = 0
        self._len = len
          
    def add(self, element: int):
        if(element is not None):
            self._buffer[self._idx] = element
            self._idx = (self._idx + 1) % self._len
        
    def get(self, stride = 5):
        """Get every element, ordered, with given stride"""
        ordered = np.concatenate((self._buffer[self._idx:], self._buffer[:self._idx]))
        return ordered[::-stride]