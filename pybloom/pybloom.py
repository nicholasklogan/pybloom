#pybloom.py
#Charles J. Lai
#October 12, 2013

from pyhash import fnv_1a

"""
See readme for more information.
"""

class BloomFilter:
    """
    Class: A conceptual implmentation of a bloom filter. 

    Disclaimer: Not a true bloom filter as the bit array in this class takes
    up more memory than a true array of bits. This implmentation uses a list
    as an abstraction of a bit array.
	"""

    #Fields (Hidden)
    _size = 0
    _hash_count = 0
    _bit_array = []

    #Immutable properties
    @property
    def size(self):
        """
        This is the size of the bloom filter i.e. the number of bits of the
        filter.
        """
        return self._size

    @property
    def hash_count(self):
        """
        This is the number of k hash function in the bloom filter.
        """
        return self._hash_count

    @property
    def bit_array(self):
        """
        This is the bit array abstraction of the bloom filter itself.
        """
        return self._bit_array

    #Built-in Methods
    def __init__(self, m, k):
        """
        Constructor: Creates a bloom filter with size m bits and k hash
        functions.
        """
        self._size = m
        self._hash_count = k
        #Initialize an array of 0 bits of size m. Our array is a list.
        self._bit_array = [0 for bin in range(self.size)]

    def add(self, string):
        """
        Procedure: Adds a string or list of strings into the bloom filter.
        """
        #Case 1: string is a single string literal
        if type(string) == str:
            for seed in xrange(self.hash_count):
                result = int(fnv_1a(string, seed) % self.size)
                self.bit_array[result] = 1
        #Case 2: string is a list of strings
        if type(string) == list:
            word_list = string
            for word in word_list:
                for seed in xrange(self.hash_count):
                    result = int(fnv_1a(word, seed) % self.size)
                    self.bit_array[result] = 1
            
    def test(self, string):
        """
        Returns: True if the word is probably in the filter and False
        if the word is definitely not in the bloom filter.
        """
        for seed in xrange(self.hash_count):
            result = int(fnv_1a(string, seed) % self.size)
            if self.bit_array[result] == 0:
                return False
        return True


#=========================================================================
#                       Various Implementations
#=========================================================================
class SpellChecker(BloomFilter):

    def __init__(self, m, k, word_list_file):
        word_list = open(word_list_file).read().lower().split(" ")
        BloomFilter.__init__(self, m, k)
        self.add(word_list)

    def find_mispellings(self, string):
        #Initialize list of words and empty list of mispelled words
        mispelled_words = []
        word_list = string.lower().split(" ")

        #Test each word in the list of words
        for word in word_list:
            for seed in xrange(self.hash_count):
                result = int(fnv_1a(word, seed) % self.size)
                #If a word is hashed to a 0 bit, add it to mispelled_words
                if self.bit_array[result] == 0:
                    mispelled_words.append(word)
                    break;
        return mispelled_words


class SheSaidFilter(BloomFilter):
    def __init__(self, m, k, words_she_said):
        word_list = open(words_she_said).read().split(" ")
        BloomFilter.__init__(self, m, k)
        self.add(word_list)

    def did_she_say(self, string):
        """
        Returns: True if that's what she said. False if that's not what
        she said.
        """
        #Initialize list of words and she_said_coefficient (SSC)
        she_said_coefficient = 0
        word_list = string.lower().split(" ")

        #Test each word in the list of words
        for word in word_list:
            word_in_filter = True
            for seed in xrange(self.hash_count):
                result = int(fnv_1a(word, seed) % self.size)
                #If a word is hashed to a 0 bit, break and test next word
                if self.bit_array[result] == 0:
                    word_in_filter = False
                    break;
            #If the word is hashed to all 1 bits, increment SSC by 1
            if word_in_filter:
                she_said_coefficient += 1
        if she_said_coefficient > 2:
            print "That's what she said."
            return True
        else:
            print "That's not what she said."
            return False

#==============================================
#               Testing App
#==============================================
def main():
    """
    Testing Function
    """
    pass


if __name__ == '__main__':
    main()