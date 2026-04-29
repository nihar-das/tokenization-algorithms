from collections import Counter


def pre_tokenize(text):
    tokens = text.encode("utf-8")  # tokens is collection of raw byte
    tokens = list(map(int, tokens))  # converts raw byte to integer between 0-255
    return tokens


class BytePairEncoding:
    def __init__(self, text):
        self.text = text
        self.tokens = pre_tokenize(text)
        self.new_id = 256
        self.merge_history = {}
        self.token2byte = {i: bytes([i]) for i in range(0, 256)}

    def get_pair_frequency(self, ids):
        all_pairs = list(zip(ids, ids[1:]))
        counter = Counter(all_pairs)
        return counter

    def merge(self, ids, id_pair, new_id):
        new_ids = []
        i = 0
        while i < len(ids):
            if i < (len(ids) - 1) and ids[i] == id_pair[0] and ids[i + 1] == id_pair[1]:
                new_ids.append(new_id)
                i += 2
            else:
                new_ids.append(ids[i])
                i += 1
        return new_ids

    def vocab_update(self, merges=5):
        for _ in range(merges):
            pair_freq = self.get_pair_frequency(self.tokens)

            if not pair_freq:
                break

            pair, _ = pair_freq.most_common()[0]
            self.tokens = self.merge(self.tokens, pair, self.new_id)
            self.token2byte[self.new_id] = (
                self.token2byte[pair[0]] + self.token2byte[pair[1]]
            )
            self.merge_history[pair] = self.new_id
            self.new_id += 1

    def encode(self, text):
        ip_tokens = pre_tokenize(text)
        while len(ip_tokens) >= 2:
            pairs = self.get_pair_frequency(ip_tokens)
            pair = min(pairs, key=(lambda p: self.merge_history.get(p, float("inf"))))

            if pair not in self.merge_history:
                break

            ip_tokens = self.merge(ip_tokens, pair, self.merge_history[pair])

        return ip_tokens

    def decode(self, tokens):
        if len(tokens):
            token_bytes = [self.token2byte[token] for token in tokens]
            text = b"".join(token_bytes)
            text = text.decode("utf-8", errors="replace")
            return text
        return tokens
