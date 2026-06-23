# Note: This file is used for Task 4.4 only
from data_structures.array_max_heap import ArrayMaxHeap
from data_structures.hash_table_separate_chaining import HashTableSeparateChaining

class RewardEntry:
    def __init__(self, reward, location_name):
        self.reward = reward
        self.location_name = location_name

    def __gt__(self, other):
        if self.reward > other.reward:
            return True

        if self.reward < other.reward:
            return False

        return self.location_name < other.location_name

    def __ge__(self, other):
        return self > other or self == other

    def __eq__(self, other):
        return self.reward == other.reward and self.location_name == other.location_name

    def __str__(self):
        return "(" + str(self.reward) + ", " + self.location_name + ")"


class RewardStatus:
    def __init__(self, location, reward):
        self.location = location
        self.reward = reward
        self.visited = False


class RewardMaxHeap(ArrayMaxHeap):
    def __init__(self, max_items):
        ArrayMaxHeap.__init__(self, max_items)
        self.positions = HashTableSeparateChaining(max_items * 2 + 1)

    def add_unordered(self, entry):
        """
        Add an entry to the heap array without rising it.
        """
        if self.is_full():
            raise ValueError("Cannot add to full heap.")

        self._length += 1
        self._array[self._length] = entry
        self.positions[entry.location_name] = self._length

    def heapify_structure(self):
        """
        Restore the heap property after unordered insertion.
        """
        for index in range(len(self) // 2, 0, -1):
            self._sink(index)

    def extract_max(self):
        """
        Extract and return the maximum reward entry.
        """
        return self.extract_root()

    def extract_root(self):
        if self._length == 0:
            raise ValueError("We cannot extract_root from empty heap.")

        result = self._array[1]
        del self.positions[result.location_name]

        if self._length == 1:
            self._array[1] = None
            self._length = 0
            return result

        last_item = self._array[self._length]
        self._array[self._length] = None
        self._length -= 1

        self._array[1] = last_item
        self.positions[last_item.location_name] = 1
        self._sink(1)

        return result

    def update_reward(self, location_name, new_reward):
        """
        Update the reward for an unvisited location already inside the heap.
        """
        index = self.positions[location_name]
        self._array[index].reward = new_reward

        if index > 1 and self._array[index] > self._array[index // 2]:
            self._rise(index)
        else:
            self._sink(index)

    def _rise(self, index):
        rising_item = self._array[index]

        while index > 1 and rising_item > self._array[index // 2]:
            self._array[index] = self._array[index // 2]
            self.positions[self._array[index].location_name] = index
            index = index // 2

        self._array[index] = rising_item
        self.positions[rising_item.location_name] = index

    def _sink(self, index):
        sinking_item = self._array[index]

        while 2 * index <= len(self):
            child_index = self._get_child_index(index)

            if sinking_item >= self._array[child_index]:
                break

            self._array[index] = self._array[child_index]
            self.positions[self._array[index].location_name] = index
            index = child_index

        self._array[index] = sinking_item
        self.positions[sinking_item.location_name] = index