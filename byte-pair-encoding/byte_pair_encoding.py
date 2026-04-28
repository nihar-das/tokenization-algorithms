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
        self.merge_history = None

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
        for word in self.word_chars.keys():
            chars = self.word_chars[word]
            for i in range(0, len(chars) - 1):
                pair = (chars[i], chars[i + 1])
                if pair not in char_pairs:
                    char_pairs.append(pair)
        self.char_pairs = char_pairs

    def score_all_pair(self):
        all_pair_scores = {}
        for target_pair in self.char_pairs:
            all_pair_scores[target_pair] = 0
            for word in self.word_chars.keys():
                word_pairs = list(zip(self.word_chars[word], self.word_chars[word][1:]))
                pair_counter = Counter(word_pairs)
                all_pair_scores[target_pair] += (
                    pair_counter[target_pair] * self.word_freq[word]
                )
        self.all_pair_scores = all_pair_scores

    def build_score_heap(self):
        if self.all_pair_scores:
            nodes = [
                MaxHeapNode(self.all_pair_scores[pair], pair)
                for pair in self.all_pair_scores.keys()
            ]
            heap = MaxHeap(nodes)
            heap.build_heap()
            self.score_heap = heap

    def merge_pair(self, pair, joined_pair, word_list):
        new_word_list = []
        i = 0
        while i < len(word_list):
            if (
                i < (len(word_list) - 1)
                and word_list[i] == pair[0]
                and word_list[i + 1] == pair[1]
            ):
                new_word_list.append(joined_pair)
                i += 2
            else:
                new_word_list.append(word_list[i])
                i += 1
        return new_word_list

    """
    compute new pairs -> score new pairs
    compute new, existing and stale node by comparing
        - pair<->score map
        - pair<->index map (heap)
    new: score_pairs - heap_pairs
    stale: heap_pairs - score_pairs
    existing: score_pairs n heap_pairs
    """

    def update_heap(self):
        self.compute_char_pair()
        self.score_all_pair()
        pair_index_map = self.score_heap.pair2index()

        heap_pairs = set(pair_index_map.keys())
        score_pairs = set(self.all_pair_scores.keys())

        new_pairs = score_pairs - heap_pairs
        stale_pairs = heap_pairs - score_pairs
        existing_pair = score_pairs & heap_pairs

        # FIXME: Setting score to 0 causes memory leak as inactive nodes pile up.
        # Fix: Recreate the max_heap array entirely with active pairs instead of set ops.
        for pair in stale_pairs:
            pair_idx = pair_index_map[pair]
            self.score_heap.max_heap[pair_idx].score = 0

        for pair in existing_pair:
            pair_idx = pair_index_map[pair]
            self.score_heap.max_heap[pair_idx].score = self.all_pair_scores[pair]

        for pair in new_pairs:
            self.score_heap.insert(MaxHeapNode(self.all_pair_scores[pair], pair))

        self.score_heap.build_heap()

    def vocab_update(self, merges=5):
        i = merges
        while i:
            node = self.score_heap.extract()
            pair = node.pair
            joined_pair = "".join(pair)

            # merge the pair in every word if exists
            for word in self.word_chars.keys():
                # merge in word_char list
                self.word_chars[word] = self.merge_pair(
                    pair, joined_pair, self.word_chars[word]
                )
            # merge in vocab
            self.vocabs.append(joined_pair)
            i -= 1
            # store every merge operation
            if self.merge_history is None:
                self.merge_history = [{pair: joined_pair}]
            else:
                self.merge_history.append({pair: joined_pair})

            self.update_heap()
