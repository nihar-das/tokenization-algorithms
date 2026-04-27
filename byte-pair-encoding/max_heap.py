class MaxHeapNode:
    def __init__(self, score=0, pair=None):
        self.score = score
        self.pair = pair


class MaxHeap:
    def __init__(self, items):
        self.max_heap = items
        self.item_count = len(items)

    def get_largest(self, root_idx):
        largest_idx = root_idx
        current_node = self.max_heap[root_idx]
        max_score = current_node.score
        left_idx = (2 * root_idx) + 1
        right_idx = left_idx + 1

        # check boundary condition of indices
        if left_idx < self.item_count and self.max_heap[left_idx].score > max_score:
            largest_idx = (2 * root_idx) + 1
            max_score = self.max_heap[left_idx].score
        if right_idx < self.item_count and self.max_heap[right_idx].score > max_score:
            largest_idx = 2 * (root_idx + 1)
            max_score = self.max_heap[right_idx].score

        return largest_idx

    def heapify(self, root_idx):
        largest_idx = self.get_largest(root_idx)

        if largest_idx == root_idx:
            return

        # swap root and largest
        self.max_heap[root_idx], self.max_heap[largest_idx] = (
            self.max_heap[largest_idx],
            self.max_heap[root_idx],
        )

        self.heapify(largest_idx)

    def build_heap(self):
        # starting from last internal node
        start_idx = (self.item_count // 2) - 1

        while start_idx >= 0:
            self.heapify(start_idx)
            start_idx -= 1

    def extract(self):
        self.max_heap[0], self.max_heap[self.item_count - 1] = (
            self.max_heap[self.item_count - 1],
            self.max_heap[0],
        )
        target_item = self.max_heap[self.item_count - 1]
        self.item_count -= 1
        self.heapify(0)
        return target_item
