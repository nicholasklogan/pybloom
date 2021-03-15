"""
pybloom.py
Original Author: Charles J. Lai
October 12, 2013

Updated: Nicholas Logan
March 14, 2021

See readme for more information. Or check out the wikipedia entry.
"""

from fnvhash import fnv1a_32


# General bloom filter class implementation
class BloomFilter:
    """
    Class: A conceptual implementation of a bloom filter.

    Disclaimer: Not a true bloom filter as the bit array in this class takes
    up more memory than a true array of bits. This implementation uses a list
    as an abstraction of a bit array."""

    def __init__(self, m, k):
        """
        Constructor: Creates a Bloom filter with size m bits and k hash
        functions.
        """
        self.size = m
        self.hash_count = k
        #Initialize an array of 0 bits of size m. Our array is a list.
        self.bit_array = [0 for _ in range(self.size)]

    def add(self, string):
        """
        Procedure: Adds a string or list of strings into the bloom filter.
        """
        # Case 1: string is a single string literal
        if isinstance(string, str):
            self.add_str(string)

        # Case 2: string is a list of strings
        if isinstance(string, list):
            self.add_iter(string)

    def add_str(self, string):
        for seed in range(self.hash_count):
            self.bit_array[self.bit_index(string, seed)] = 1

    def add_iter(self, iterator):
        for word in iterator:
            self.add_str(word)

    def test(self, string):
        """
        Returns: True if the word is probably in the filter and False
        if the word is definitely not in the bloom filter.
        """
        return all(self.bit_in_filter(string, seed) for seed in range(self.hash_count))

    def bit_in_filter(self, string, seed):
        return self.bit_value(string, seed) == 1

    def word_in_filter(self, word):
        return all(self.bit_in_filter(word, seed) for seed in range(self.hash_count))

    def bit_index(self, string, seed):
        return int(fnv1a_32(string, seed) % self.size)

    def bit_value(self, string, seed):
        return self.bit_array[self.bit_index(string, seed)]


# Bloom filter implementations
class SpellChecker(BloomFilter):
    """
    An bloom filter implementation of a spell checker.
    """

    def __init__(self, m, k, word_list_file):
        super(self, SpellChecker).__init__(m, k)
        with open(word_list_file) as f:
            self.add(f.read().lower().split(" "))

    def find_mispellings(self, string):
        return [word for word in string.lower().split(" ") if not self.word_in_filter(word)]


class SheSaidFilter(SpellChecker):  # Set as SpellChecker to reuse the __init__ method
    """
    A naive Bloom filter implementation of a that's what she said checker.
    """

    def did_she_say(self, input, SSC=3):
        """
        Returns: True if that's what she said. False if that's not what
        she said.

        The SSC variable is a user defined option to alter the sensitivity
        of the filter.
        """
        #Initialize list of words and the she_said_coefficient (SSC)
        she_said_coefficient = sum(1 for word in input.lower().split(" ") if self.word_in_filter(word))

        if she_said_coefficient > SSC:
            print("That's what she said.")
            return True
        else:
            print("That's not what she said.")
            return False


#== Testing Application ==================================================
def main():
    """
    Testing Function
    """


if __name__ == '__main__':
    main()