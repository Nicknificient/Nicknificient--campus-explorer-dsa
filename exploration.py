from campus import Campus

class Exploration:
    def __init__(self, campus_name):
        self.campus = Campus(campus_name)

    def greedy_student(self, location, stamina):
        """
        Time complexity:
        Let S be the stamina value
        Let D be the maximum number of outgoing connection from any location.
        Best case: O(1)
        The best case happen when the starting location has no outgoing connection,
        or when stamina is 0. In that case, the method only get the reward of the
        current location and return, so the time complexity is O(1).

        Worst case: O(S * D)
        The worst case happen when the student keeps moving until the stamina runs out.
        At each visited location, the method check all outgoing connections to find the
        best next location. This takes O(D) time per recursive call. Since stamina is
        reduced by 1 each time, there can be at most S recursive steps.
        Therefore, the worst-case time complexity is O(S * D).
        """
        total_reward = location.get_reward()

        if stamina == 0:
            return total_reward

        best_connection = None

        for connection in location.get_connections():
            if best_connection is None:
                best_connection = connection
            else:
                current_difficulty = connection.get_difficulty()
                best_difficulty = best_connection.get_difficulty()

                current_reward = connection.get_location().get_reward()
                best_reward = best_connection.get_location().get_reward()

                if current_difficulty < best_difficulty:
                    best_connection = connection
                elif current_difficulty == best_difficulty and current_reward > best_reward:
                    best_connection = connection

        if best_connection is None:
            return total_reward

        return total_reward + self.greedy_student(
            best_connection.get_location(),
            stamina - 1
        )

    def total_difficulty(self, location):
        """
        Time complexity analysis not required for this method.
        """
        return self._total_difficulty_helper(location)[1]

    def _total_difficulty_helper(self, location):
        """
        number of complete paths from this location to final locations
        sum of difficulties across all those complete paths
        """
        path_count = 0
        difficulty_sum = 0

        for connection in location.get_connections():
            child_path_count, child_difficulty_sum = self._total_difficulty_helper(
                connection.get_location()
            )

            path_count += child_path_count
            difficulty_sum += child_difficulty_sum + (
                connection.get_difficulty() * child_path_count
            )

        if path_count == 0:
            return 1, 0

        return path_count, difficulty_sum

    def total_reward_for_longest_path(self, location):
        """
        Time complexity analysis not required for this method.
        """
        return self._longest_path_helper(location)[1]

    def _longest_path_helper(self, location):
        """
        length of the longest path from this location
        maximum reward for that longest path
        """
        best_length = 1
        best_reward = location.get_reward()

        for connection in location.get_connections():
            child_length, child_reward = self._longest_path_helper(
                connection.get_location()
            )

            current_length = child_length + 1
            current_reward = child_reward + location.get_reward()

            if current_length > best_length:
                best_length = current_length
                best_reward = current_reward
            elif current_length == best_length and current_reward > best_reward:
                best_reward = current_reward

        return best_length, best_reward

    def __str__(self):
        """
        Optional: For debugging purposes only
        """
        return str(self.campus)

if __name__ == '__main__':
    print("Clayton")
    clayton = Exploration("clayton")
    for campus_location in clayton.campus.get_all_locations():
        print(campus_location)
    print()

    print("Malaysia")
    malaysia = Exploration("malaysia")
    for campus_location in malaysia.campus.get_all_locations():
        print(campus_location)

    # Sample test cases
    assert clayton.greedy_student(clayton.campus.get_location_by_name('Menzies Building'), 1) == 22, "Greedy student should collect 22 reward"
    assert clayton.total_difficulty(clayton.campus.get_start_location()) == 190, "Total difficulty should be 190"
    assert clayton.total_reward_for_longest_path(clayton.campus.get_start_location()) == 86, "Longest path should be 86"

    # Add test code here
    assert clayton.greedy_student(clayton.campus.get_start_location(), 2) == 29, "Greedy student from Campus Centre with stamina 2 should collect 29"
    assert clayton.total_reward_for_longest_path(clayton.campus.get_location_by_name('Menzies Building')) == 65, "Longest path from Menzies Building should collect 65"