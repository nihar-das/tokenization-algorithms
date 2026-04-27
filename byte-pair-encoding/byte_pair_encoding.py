from collections import Counter
from max_heap import MaxHeapNode, MaxHeap


class BytePairEncoding:
    def __init__(self, text):
        self.text = text
        self.word_freq = None
        self.word_chars = None
        self.vocabs = None
        self.char_pairs = None
        self.all_pair_scores = None
        self.score_heap = None

        self.text2WordFreq()
        self.word2chars()
        self.wordFreq2Vocab()
        self.compute_char_pair()
        self.score_all_pair()
        self.build_score_heap()

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

    def word2chars(self):
        word_chars = {}
        for word in self.word_freq.keys():
            word_chars[word] = [char for char in word]
        self.word_chars = word_chars

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

    def score_all_pair(self):
        all_pair_scores = {}
        for target_pair in self.char_pairs:
            all_pair_scores[target_pair] = 0
            for word in self.word_freq.keys():
                word_pairs = list(zip(word, word[1:]))
                pair_counter = Counter(word_pairs)
                all_pair_scores[target_pair] += (
                    pair_counter[target_pair] * self.word_freq[word]
                )
        self.all_pair_scores = all_pair_scores

    def build_score_heap(self):
        if self.all_pair_scores and (self.score_heap is None):
            nodes = [
                MaxHeapNode(self.all_pair_scores[pair], pair)
                for pair in self.all_pair_scores.keys()
            ]
            heap = MaxHeap(nodes)
            heap.build_heap()
            self.score_heap = heap

    def merge_pair(self, pair, word_list):
        new_word_list = []
        i = 0
        while i < len(word_list):
            if word_list[i] == pair[0] and word_list[i + 1] == pair[1]:
                new_word_list.append(pair)
                i += 2
            else:
                new_word_list.append(word_list[i])
                i += 1
        return new_word_list

    def vocab_update(self, merges=5):
        i = merges
        while i:
            node = self.score_heap.extract()
            pair = node.pair

            # merge the pair in every word if exists
            for word in self.word_chars.keys():
                joined_pair = "".join(pair)
                if joined_pair in word:
                    self.word_chars[word] = self.merge_pair(
                        joined_pair, self.word_chars[word]
                    )
            i -= 1
