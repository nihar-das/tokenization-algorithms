class MaxHeapNode:
    def __init__(self, score=0, pair=None):
        self.score = score
        self.pair = pair

    def __gt__(self, other):
        if self.score == other.score:
            return self.pair < other.pair
        return self.score > other.score


class MaxHeap:
    def __init__(self, items):
        self.max_heap = items
        self.item_count = len(items)

    def get_largest(self, root_idx):
        largest_idx = root_idx
        max_score_node = self.max_heap[root_idx]
        left_idx = (2 * root_idx) + 1
        right_idx = left_idx + 1

        # check boundary condition of indices
        if left_idx < self.item_count and self.max_heap[left_idx] > max_score_node:
            largest_idx = (2 * root_idx) + 1
            max_score_node = self.max_heap[left_idx]
        if right_idx < self.item_count and self.max_heap[right_idx] > max_score_node:
            largest_idx = 2 * (root_idx + 1)
            max_score_node = self.max_heap[right_idx]

        return largest_idx

    def heapify_down(self, root_idx):
        largest_idx = self.get_largest(root_idx)

        if largest_idx == root_idx:
            return

        # swap root and largest
        self.max_heap[root_idx], self.max_heap[largest_idx] = (
            self.max_heap[largest_idx],
            self.max_heap[root_idx],
        )

        self.heapify_down(largest_idx)

    def build_heap(self):
        # starting from last internal node
        start_idx = (self.item_count // 2) - 1

        while start_idx >= 0:
            self.heapify_down(start_idx)
            start_idx -= 1

    def insert(self, data):
        self.max_heap.append(data)
        self.item_count = len(self.max_heap)

    def extract(self):
        self.max_heap[0], self.max_heap[self.item_count - 1] = (
            self.max_heap[self.item_count - 1],
            self.max_heap[0],
        )
        target_item = self.max_heap.pop(-1)
        self.item_count = len(self.max_heap)
        self.heapify_down(0)
        return target_item

    def pair2index(self):
        pair_index_map = {}
        for idx, node in enumerate(self.max_heap):
            pair_index_map[node.pair] = idx

        return pair_index_map
