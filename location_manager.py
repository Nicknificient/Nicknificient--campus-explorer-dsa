from campus import Campus
from data_structures.binary_search_tree import BinarySearchTree
from data_structures.hash_table_separate_chaining import HashTableSeparateChaining
from data_structures.array_list import ArrayList


class LocationManager:
    def __init__(self, campus_name):
        """
        Time complexity:
        Let N be the number of locations in the campus
        Let C be the maximum number of outgoing connections from a location.
        Best case: O(N * (C + log N))
        Worst case: O(N * (C + log N))
        
        First of all,loads all locations. we then go through all
        locations once to count them, so that the hash table can be creat with a
        suitable size.

        After that, we go through the location again. For each location, we calculate
        the average difficulty by check its outgoing connection which costs
        O(C) in the worst case. The desirability calculation itself is O(1).

        Each location is insert into the BinarySearchTree using desirability as
        the main ordering value. Based on the assignment assumption, tree operations
        take O(log N). we also store the location details in a hash table, which is
        O(1).

        The best case and worst case are  O(N * (C + log N)),this is because every location still
        needs to be process and inserted.
        """
        self.campus: Campus = Campus(campus_name)
        self.locations = BinarySearchTree()

        number_of_locations = 0
        for location in self.campus.get_all_locations():
            number_of_locations += 1

        self.location_lookup = HashTableSeparateChaining(number_of_locations * 2 + 1)

        for location in self.campus.get_all_locations():
            average_difficulty = self._calculate_average_difficulty(location)
            desirability = self._calculate_desirability(location, average_difficulty)
            key = (desirability, location.get_name())

            self.locations[key] = location
            self.location_lookup[location.get_name()] = (
                location,
                desirability,
                average_difficulty
            )

    def get_locations_in_range(self, min_score, max_score):
        """
        Time complexity:
        Let N be the number of locations in the tree
        
        Let K be the number of locations returned.

        First, searches the BinarySearchTree by desirability. Since the tree is
        ordered by desirability, we does not need to visit every node when the range
        only covers a small part of the tree.
        
        Best case: O(log N + K)
        The best case happens when the range is small. In that case, the method only
        follows the relevant branches of the tree and returns the K matching
        location. This occurs when the range falls entirely to one side of the root, 
        so only one branch is followed down to depth O(log N) before all K matches are found.

        Worst case: O(N)
        The worst case happens when the range covers most or all locations. Then the
        method may need to visit every node in the tree, so the time complexity is
        O(N).

        The results are added during an in-order traversal, so they are returned in
        increasing order of desirability.
        """
        result = ArrayList()
        self._range_search(self.locations._root, min_score, max_score, result)
        return result

    def _range_search(self, current, min_score, max_score, result):
        """
        Helper for get_locations_in_range.

        This helper accesses the internal tree nodes. That is allowed for Task 3.2.
        """
        if current is None:
            return

        desirability = current.key[0]

        if desirability > min_score:
            self._range_search(current.left, min_score, max_score, result)

        if min_score <= desirability <= max_score:
            result.append((desirability, current.item.get_name()))

        if desirability < max_score:
            self._range_search(current.right, min_score, max_score, result)

    def get_top_k_locations(self, k):
        """
        Time complexity:
        Let N be the number of locations in the tree
        Let K be the input k.
        
        Best case: O(log N + K)
        Worst case: O(log N + K)

        The locations are store in a BinarySearchTree ordered by desirability in
        ascending order. To get the most desirable locations first, we do a reverse
        in-order traversal: right, node, left
        The traversal stops as soon as K locations have been add, so it does not
        process the rest of the tree unnecessarily.

        Based on the assumption, the height of the tree is O(log N).
        Reaching the largest values costs O(log N), and collecting K locations costs
        O(K).Therefore, both the best case and worst case are O(log N + K).
        """
        result = ArrayList(k)
        self._top_k_helper(self.locations._root, k, result)
        return result

    def _top_k_helper(self, current, k, result):
        """
        Helper for get_top_k_locations-accesses the internal tree nodes. That is allowed for Task 3.3.
        """
        if current is None or len(result) == k:
            return

        self._top_k_helper(current.right, k, result)

        if len(result) < k:
            result.append((current.key[0], current.item.get_name()))

        if len(result) < k:
            self._top_k_helper(current.left, k, result)

    def update_location(self, name, new_reward):
        """
        Time complexity:
        Let N be the number of locations in the tree.
        
        Best case: O(log N)
        Worst case: O(log N)

        The location is found using the hash table, which costs O(1) based on the
        assignment assumption. The old desirability value is also stored there, so we
        can remove the old entry from the BinarySearchTree without searching through
        all locations.Deleting the old tree entry costs O(log N). After updating the reward, the
        new desirability is calculated in O(1), because the average difficulty was
        already stored. The updated location is then inserted back into the tree,
        which costs O(log N). Finally, the hash table entry is updated in O(1).
        The best case and worst case are both O(log N), because the tree removal and
        insertion are needed for every update.
        """
        location, old_desirability, average_difficulty = self.location_lookup[name]

        old_key = (old_desirability, name)
        del self.locations[old_key]

        location.set_reward(new_reward)

        new_desirability = self._calculate_desirability(location, average_difficulty)
        new_key = (new_desirability, name)

        self.locations[new_key] = location
        self.location_lookup[name] = (
            location,
            new_desirability,
            average_difficulty
        )

    def _calculate_average_difficulty(self, location):
        """
        Calculate the average outgoing connection difficulty.
        If the location has no outgoing connections, the average difficulty is 0.
        """
        total_difficulty = 0
        number_of_connections = 0

        for connection in location.get_connections():
            total_difficulty += connection.get_difficulty()
            number_of_connections += 1

        if number_of_connections == 0:
            return 0

        return total_difficulty / number_of_connections

    def _calculate_desirability(self, location, average_difficulty):
        """
        Calculate the desirability score for a location.
        """
        return round(location.get_reward() / (1 + average_difficulty), 2)

    def __str__(self):
        """
        Optional: For debugging purposes only.
        """
        result = ""

        for key, location in self.locations:
            result += str(key[0]) + " " + location.get_name() + "\n"

        return result

if __name__ == '__main__':
    location_manager = LocationManager('clayton')

    # range query
    locations_in_range = location_manager.get_locations_in_range(1.5, 6.0)

    assert len(locations_in_range) == 7, "range length is wrong"
    assert locations_in_range[0] == (2.2, 'Robert Blackwood Hall'), "range first item is wrong"
    assert locations_in_range[3] == (3.6, 'Alan Finkel Building for Technology and Design'), "range middle item is wrong"
    assert locations_in_range[6] == (6.0, 'Religious Centre'), "range last item is wrong"

    # top k locations
    top_locations = location_manager.get_top_k_locations(3)

    assert len(top_locations) == 3, "top k length is wrong"
    assert top_locations[0] == (13.0, 'New Horizons'), "top k first item is wrong"
    assert top_locations[1] == (8.0, 'Monash Club'), "top k second item is wrong"
    assert top_locations[2] == (6.0, 'Religious Centre'), "top k third item is wrong"

    # dynamic update
    location_manager.update_location('Law Building and Library', 14)
    updated_range = location_manager.get_locations_in_range(3.5, 3.5)

    assert len(updated_range) == 1, "update range length is wrong"
    assert updated_range[0] == (3.5, 'Law Building and Library'), "updated location is wrong"