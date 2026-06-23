from campus import Campus
from data_structures.array_list import ArrayList
from data_structures.hash_table_separate_chaining import HashTableSeparateChaining
from reward_structure import RewardEntry
from reward_structure import RewardStatus
from reward_structure import RewardMaxHeap


class RewardSeeker:
    def __init__(self, campus_name):
        """
        Let N be the number of locations on campus.
        Best case: O(N)
        Worst case: O(N)

        First, the campus locations are loaded. we then go through all locations once to
        count them, so we can create the heap and hash table with a suitable size.
        After that, we go through the location again. Each location is add to the heap
        array without rising it, which costs O(1), and it is also added to the hash
        table in O(1).Once all locations have been add, heapify_structure() is called to build the
        heap properly. This takes O(N),this is better than inserting each location one by one using normal heap insertion.
        The best case and worst case are both O(N), because every location still needs
        to be add before the semester starts.

        """
        self.campus: Campus = Campus(campus_name)

        number_of_locations = 0
        for location in self.campus.get_all_locations():
            number_of_locations += 1

        self.rewards = RewardMaxHeap(number_of_locations)
        self.location_status = HashTableSeparateChaining(number_of_locations * 2 + 1)

        for location in self.campus.get_all_locations():
            reward = location.get_reward()
            location_name = location.get_name()

            self.rewards.add_unordered(RewardEntry(reward, location_name))
            self.location_status[location_name] = RewardStatus(location, reward)

        self.rewards.heapify_structure()

    def get_next_location(self):
        """
        Time complexity:
        Let N be the number of unvisited locations still inside the heap.

        Best case: O(1)
        This is because when the heap is empty.The method only check that there are no locations left and returns None.
        Worst case: O(log N)
        This because when there is at least one location in the heap. The
        method extracts the maximum reward entry, which may require sinking an item down
        the heap. This costs O(log N). Update the visited status in the hash table
        costs O(1).
        To summarize, the worst-case time complexity is O(log N).
        """
        if self.rewards.is_empty():
            return None

        entry = self.rewards.extract_max()
        status = self.location_status[entry.location_name]
        status.visited = True

        return (entry.reward, entry.location_name)

    def get_top_k_locations(self, k):
        """
        Time complexity:
        Let N be the number of unvisited locations in the heap
        Let k be the number of locations requested.
        
        Best case: O(1)
        This is because when the heap is already empty. The loop does not run, so
        the method just returns an empty ArrayList. This gives O(1).
        
        Worst case: O(k log N)
        This is because when there are at least k locations available. The method
        calls get_next_location() k times. Each call removes the current highest reward
        location from the heap and costs O(log N).

        Appending each result to the ArrayList is O(1), since the ArrayList is create with capacity k.
        So, the worst-case time complexity is O(k log N).
        """
        result = ArrayList(k)

        while len(result) < k and not self.rewards.is_empty():
            result.append(self.get_next_location())

        return result

    def update_location_reward(self, location_name, new_reward):
        """
        Time complexity:
        Let N be the number of unvisited locations still inside the heap.

        The location status is found using the hash table, which costs O(1). 
        The Location object reward and the save reward in the status object are then updated in O(1).
        
        Best case: O(1)
        Because when the location has already visited. Since visited
        locations are no longer in the heap, there is no heap update needed, so the
        method finishes in O(1).
        
        Worst case: O(log N)
        The worst case happens when the location is still unvisited. In that case, the
        reward must also be updated inside the heap. The heap entry may need to rise or
        sink to restore the heap order, which costs O(log N).
        """
        status = self.location_status[location_name]

        status.reward = new_reward
        status.location.set_reward(new_reward)

        if not status.visited:
            self.rewards.update_reward(location_name, new_reward)

if __name__ == '__main__':
    reward_seeker = RewardSeeker('clayton')

    # next location
    next_loc = reward_seeker.get_next_location()
    assert next_loc == (18, 'Alan Finkel Building for Technology and Design'), "next location test failed"

    # top k after one location has already been visited
    top3 = reward_seeker.get_top_k_locations(3)
    assert len(top3) == 3, "top k length test failed"
    assert top3[0] == (17, 'Learning and Teaching Building'), "top k first test failed"
    assert top3[1] == (16, 'Monash Club'), "top k second test failed"
    assert top3[2] == (15, 'Law Building and Library'), "top k third test failed"

    # update reward
    reward_seeker.update_location_reward('Campus Centre', 21)
    updated_location = reward_seeker.get_next_location()
    assert updated_location == (21, 'Campus Centre'), "update reward test failed"

    # another update test using a fresh object
    reward_seeker2 = RewardSeeker('clayton')
    reward_seeker2.get_top_k_locations(2)

    reward_seeker2.update_location_reward('Religious Centre', 19)
    reward_seeker2.update_location_reward('Campus Centre', 21)

    top_updated = reward_seeker2.get_top_k_locations(2)
    assert top_updated[0] == (21, 'Campus Centre'), "updated top k first test failed"
    assert top_updated[1] == (19, 'Religious Centre'), "updated top k second test failed"