from __future__ import annotations
from data_structures import ArrayList
from data_structures import LinkedList
from data_structures import HashTableSeparateChaining
import os

class Location:
    def __init__(self, name: str, building_id: str, location_type: str, floors: int, features: str, reward: int) -> None:
        self._name = name
        self._building_id = building_id
        self._location_type = location_type
        self._floors = floors

        self._features = LinkedList()
        for feature in features.split(','):
            self._features.append(feature)

        self._connections = LinkedList()
        self._reward = reward

    def get_name(self) -> str:
        return self._name

    def get_features(self) -> LinkedList:
        """
        A list of the features at this location
        """
        return self._features

    def get_location(self) -> str:
        return self._location_type

    def get_connections(self) -> LinkedList:
        """
        A list of outgoing connections from this location
        :return:
        """
        return self._connections

    def get_reward(self) -> int:
        return self._reward

    def set_reward(self, reward) -> None:
        self._reward = reward

    def __str__(self) -> str:
        return (
            f"Location({self.get_name()!r}, features={self.get_features()}, "
            f"connections={self.get_connections()}, reward={self.get_reward()})"
        )

class Connection:
    def __init__(self, location: Location, difficulty: int) -> None:
        self._location = location
        self._difficulty = difficulty

    def get_location(self) -> Location:
        return self._location

    def get_difficulty(self) -> int:
        return self._difficulty

    def __str__(self) -> str:
        return f"Connection(-> {self._location.get_name()!r}, difficulty={self.get_difficulty()})"


class Campus:
    def __init__(self, campus_name: str) -> None:
        self._start_location = None
        self._locations = LinkedList()
        self.load_campus(campus_name)

    def load_campus(self, campus_name: str) -> None:
        lookup = HashTableSeparateChaining()
        section = None

        path = os.path.join("campuses", f"{campus_name}.txt")
        if not os.path.exists(path):
            raise FileNotFoundError(f"Campus file not found: {path}")

        with open(path, "r", encoding="utf-8") as f:
            for raw in f:
                line = raw.strip()

                if not line or line.startswith('#'):
                    continue

                if line == '[Locations]':
                    section = 'locations'
                    continue

                if line == '[Connections]':
                    section = 'connections'
                    continue

                if section == 'locations':
                    parts = line.split('|')
                    if len(parts) != 6:
                        raise ValueError(f"Invalid location line: {line}")

                    name, building_id, location_type, floors, features, reward = parts
                    loc = Location(name, building_id, location_type, int(floors), features, int(reward))

                    self._locations.append(loc)
                    lookup[name] = loc

                    if self._start_location is None:
                        self._start_location = loc

                elif section == 'connections':
                    parts = line.split('|')
                    if len(parts) != 3:
                        raise ValueError(f"Invalid connection line: {line}")

                    from_name, to_name, difficulty = parts

                    if from_name not in lookup:
                        raise ValueError(f"Unknown from location: {from_name}")
                    if to_name not in lookup:
                        raise ValueError(f"Unknown to location: {to_name}")

                    conn = Connection(lookup[to_name], int(difficulty))
                    lookup[from_name].get_connections().append(conn)

        self._lookup = lookup
        if self._start_location is None:
            raise ValueError(f"No locations found in campus file: {path}")

    def get_start_location(self) -> Location:
        return self._start_location

    def get_location_by_name(self, name: str) -> Location:
        return self._lookup[name]

    def get_all_locations(self) -> LinkedList:
        return self._locations

    def __str__(self) -> str:
        return f"Campus(start_location={self._start_location.name!r})"

class Player:
    def __init__(self, player_name: str, player_id: int, score: int, stamina: int) -> None:
        self.name = player_name
        self.id = player_id
        self.score = score
        self.stamina = stamina

    def __str__(self):
        return f"{self.id:>4} {self.name:10} {self.score:>5} {self.stamina:>7}"

class LeaderboardReader:
    @staticmethod
    def read(campus_name: str) -> ArrayList[Player]:
        """
        :complexity: O(n) where n is the filesize of the leaderboard
        """
        path = os.path.join("leaderboard", f"{campus_name}.txt")
        if not os.path.exists(path):
            raise FileNotFoundError(f"Leaderboard file not found: {path}")

        with open(path) as f:
            lines = f.readlines()

        players = ArrayList(len(lines))
        for line in lines:
            player_id, name, score, stamina = line.strip().split(",")
            player = Player(name, int(player_id), int(score), int(stamina))
            players.append(player)

        return players