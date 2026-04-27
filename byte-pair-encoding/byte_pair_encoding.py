from collections import Counter
from dll import DoublyLinkedList


class BytePairEncoding:
    def __init__(self, text):
        self.text = text
        self.word_freq = None
        self.word_dll = None
        self.vocabs = None
        self.char_pairs = None

        self.text2WordFreq()
        self.word2dll()
        self.wordFreq2Vocab()
        self.compute_char_pair()

    def text2WordFreq(self):
        if self.word_freq is None:
            word_freq = {}
            for word in self.text.split(" "):
                act_word = f"{word}_"
                if act_word not in word_freq:
                    word_freq[act_word] = 1
                else:
                    word_freq[act_word] += 1
            self.word_freq = word_freq

    def word2dll(self):
        if self.word_dll is None:
            word_dll = {}
            for word in self.word_freq.keys():
                dll = DoublyLinkedList()
                for char in word:
                    dll.insert(char)
                word_dll[word] = dll
            self.word_dll = word_dll

    def wordFreq2Vocab(self):
        if self.vocabs is None:
            vocabs = []
            for word in self.word_freq.keys():
                for char in word:
                    if char not in vocabs:
                        vocabs.append(char)
            self.vocabs = vocabs

    def compute_char_pair(self):
        char_pairs = []
        if self.char_pairs is None:
            for word in self.word_freq.keys():
                for i in range(0, len(word) - 1):
                    pair = (word[i], word[i + 1])
                    if pair not in char_pairs:
                        char_pairs.append(pair)
            self.char_pairs = char_pairs

    def score_pair(self, target_pair):
        score = 0
        for word in self.word_freq.keys():
            word_pairs = list(zip(word, word[1:]))
            pair_counter = Counter(word_pairs)
            score += pair_counter[target_pair] * self.word_freq[word]
        return score
