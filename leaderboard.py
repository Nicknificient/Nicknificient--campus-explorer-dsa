from campus import LeaderboardReader
from data_structures.array_list import ArrayList
from algorithms.merge_sort import merge_sort


class Leaderboard:
    def __init__(self, campus_name):
        """
        Time complexity:
        Let N be the number of players in the leaderboard file.
        
        Best case: O(N log N)
        Worst case: O(N log N)

        First, LeaderboardReader reads all players into an ArrayList, which takes O(N) time. 
        Then, merge_sort is used to sort the players by score in descending order, 
        and then by stamina in descending order. The key function only accesses player
        attributes, so each key calculation is O(1).
        
        The best case and worst case are both O(N log N), thi is because merge sort
        divide and merges the data in the same general way doesn't matter whether the
        player are already in the correct order or not.
        Since O(N log N) dominates O(N), the overall time complexity is O(N log N).
        """
        list_of_players = LeaderboardReader.read(campus_name)

        self.players = merge_sort(
            list_of_players,
            key=lambda player: (-player.score, -player.stamina)
        )

    def combine(self, other_leaderboard):
        """
        Time complexity:

        Let N be the number of players in the current leaderboard
        Let M be the number of players in other_leaderboard
        Since both leaderboards are already sorted, so we combines them using one
        linear merge pass. Each player from both leaderboard is appended to the new
        ArrayList exactly once.

        Best case: O(N + M)
        The best case is O(N + M), because even if all players from one leaderboard
        come before the other, we still needs to copy every player into the
        combined ArrayList.
        
        Worst case: O(N + M)
        The worst case is also O(N + M). This happens when players from the two
        leaderboard are mix together throughout the merge, but each player is still
        check and append at most once.If two players have the same score and stamina, the player from the current
        leaderboard is add first. This keeps the combine operation stable,
        so the overall time complexity is O(N + M).
        """
        current_index = 0
        other_index = 0

        current_players = self.players
        other_players = other_leaderboard.players

        combined_players = ArrayList(len(current_players) + len(other_players))

        while current_index < len(current_players) and other_index < len(other_players):
            current_player = current_players[current_index]
            other_player = other_players[other_index]

            if self._comes_before_or_equal(current_player, other_player):
                combined_players.append(current_player)
                current_index += 1
            else:
                combined_players.append(other_player)
                other_index += 1

        while current_index < len(current_players):
            combined_players.append(current_players[current_index])
            current_index += 1

        while other_index < len(other_players):
            combined_players.append(other_players[other_index])
            other_index += 1

        self.players = combined_players

    def _comes_before_or_equal(self, player_one, player_two):
        """
        Return True if player_one should appear before player_two according to the leaderboard ranking rules.
        """
        if player_one.score > player_two.score:
            return True

        if player_one.score < player_two.score:
            return False

        if player_one.stamina > player_two.stamina:
            return True

        if player_one.stamina < player_two.stamina:
            return False

        return True

    def __str__(self):
        """
        Optional: For debugging purposes only
        """
        result = ""

        for player in self.players:
            result += str(player) + "\n"

        return result



if __name__ == "__main__":
    clayton = Leaderboard("clayton")
    malaysia = Leaderboard("malaysia")
    # Add test code here
    # sorting
    assert clayton.players[0].score >= clayton.players[1].score, "score order is wrong"
    assert malaysia.players[0].score >= malaysia.players[1].score, "score order is wrong"

    # same score should have higher stamina first
    for i in range(len(clayton.players) - 1):
        if clayton.players[i].score == clayton.players[i + 1].score:
            assert clayton.players[i].stamina >= clayton.players[i + 1].stamina, "stamina order is wrong"

    # combine
    clayton.combine(malaysia)
    assert len(clayton.players) > len(malaysia.players), "combine did not add players"
    for i in range(len(clayton.players) - 1):
        assert clayton.players[i].score > clayton.players[i + 1].score or (clayton.players[i].score == clayton.players[i + 1].score
        and clayton.players[i].stamina >= clayton.players[i + 1].stamina), "score/stamina order wrong after combine"