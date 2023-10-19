from __future__ import annotations
from dataclasses import dataclass
from island import Island
from data_structures.hash_table import LinearProbeTable
from data_structures.heap import MaxHeap

@dataclass
class KeyDict:
    name: str
    score: float

    def __ge__(a: KeyDict, b: KeyDict):
        """
        Magic method greater than equal
        Compare two KeyStore based on their moneymarine ratio

        :complexity: O(1), all the operations are of constant time
        """
        return (a.score >= b.score)
    
    def __gt__(a: KeyDict, b: KeyDict):
        """
        Magic method greater than
        Compare two KeyStore based on their moneymarine ratio

        :complexity: O(1), all the operations are of constant time
        """
        return (a.score > b.score)
        
    def __le__(a: KeyDict, b: KeyDict):
        """
        Magic method less than equal
        Compare two KeyStore based on their moneymarine ratio

        :complexity: O(1), all the operations are of constant time
        """
        return (a.score <= b.score)
    
    def __lt__(a: KeyDict, b: KeyDict):
        """
        Magic method less than
        Compare two KeyStore based on their moneymarine ratio

        :complexity: O(1), all the operations are of constant time
        """
        return (a.score < b.score)

class Mode2Navigator:
    """
    Student-TODO: short paragraph as per https://edstem.org/au/courses/12108/lessons/42810/slides/294117
    """

    def __init__(self, n_pirates: int) -> None:
        """
        Initialise the Mode2 NaviGator Class
        """
        self.n_pirates = n_pirates
        # Create a Linear Hash Table to store the island
        self.island_store: LinearProbeTable[str,Island] = LinearProbeTable()

    def add_islands(self, islands: list[Island]):
        """
        Add islands to the seas

        :complexity: O(I) where I is the length of Islands
        """
        # add the island in the 'islands' list into the island_store dict
        for island in islands:
            self.island_store[island.name] = island

    def simulate_day(self, crew: int) -> list[tuple[Island|None, int]]:
        """
        Simulate a day of Davy Back Fight and return a list of tuples, representing
        the choices made by the first, second, ... captain in order. Each tuple contain the
        island that was plundered and crew-mates that were sent onto the island
        """
        res: list[tuple[Island|None, int]] = []
        crew_available = crew
        sorted_key = MaxHeap(len(self.island_store))

        # O(Nlog(N))
        for island in self.island_store.values():
            marine = island.marines
            money = island.money
            crew_left = crew_available-marine
            try:
                key_immediate = money/marine*min(crew_available,marine)+2*max(0, crew_left)
            except ZeroDivisionError:   # handle situation for an island with zero marine left
                key_immediate = 2*max(0, crew_left)
            key = KeyDict(island.name, key_immediate)
            sorted_key.add(key)

        # O(C*log(N))
        for _ in range(self.n_pirates):
            # still have island that contains money
            if len(sorted_key) != 0:
                tar_key_immediate:KeyDict = sorted_key.get_max()
                tar_key = tar_key_immediate.name
                tar_island: Island = self.island_store[tar_key]
                marine = tar_island.marines
                money = tar_island.money
                mm_ratio = money/marine
                # no looting will have higher score
                if mm_ratio < 2:
                    res.append((None, 0))
                # looting to get higher score
                else:
                    crew_left = crew_available-marine   # marine is the crew required to loot the whole island
                    # have enough crew to loot the whole island (other crew wont come back and loot this island since its resources is completely loop)
                    if crew_left >= 0:
                        score = 2*crew_left + money
                        updated_island = Island(tar_island.name, 0, 0)
                        self.island_store[tar_island.name] = updated_island
                        res.append((updated_island, marine))
                        continue
                    # not enough crew to loot the whole island
                    else:
                        score = crew_available*money/marine
                        marine_left = marine - crew_available
                        money_left = money-score
                        updated_crew_left = crew_available-marine_left
                        updated_island = Island(tar_island.name, money_left, marine_left)
                        res.append((updated_island, crew_available))
                        self.island_store[tar_key] = updated_island
                        updated_key_immediate = money_left/marine_left*min(crew_available,marine_left)+2*max(0, updated_crew_left)
                        updated_key = KeyDict(tar_island.name, updated_key_immediate)
                        sorted_key.add(updated_key)

            # all the island is robbed
            else:
                res.append((None, 0))
        return res

    

    def update_island(self, island: Island, new_money: float, new_marines: int) -> None:
        """
        Student-TODO: Best/Worst Case
        """
        old_key = island.money/island.marines
        old_name = island.name
        updated_island:Island = Island(old_name, new_money, new_marines)
        updated_key = new_money/new_marines
        del self.island_store[old_key]
        self.island_store[updated_key] = updated_island


if __name__ == "__main__":
    a = Island("A", 400, 100)
    b = Island("B", 300, 150)
    c = Island("C", 100, 5)
    d = Island("D", 350, 90)
    e = Island("E", 300, 100)
    islands: list = [a, b, c, d, e]
    nav = Mode2Navigator(8)
    nav.add_islands(islands)
    print(nav.island_store)
    results = nav.simulate_day(100)
    print(results)
    print(nav.island_store)

    expected_scores = [400, 370, 300, 290, 200, 200, 200, 200]
    cur_marines = {
            island.name: island.marines
            for island in islands
        }
    cur_money = {
        island.name: island.money
        for island in islands
    }
    for (island, sent_crew), expected in zip(results, expected_scores):
        if island is None:
            print(expected==200)
            continue
        money = cur_money[island.name]
        marines = cur_marines[island.name]
        if marines == 0:
            received = money
        else:
            received = min(money, money * sent_crew / marines)
        # Update Island
        cur_money[island.name] = money - received
        cur_marines[island.name] = max(0, marines - sent_crew)
        # Score
        score = 2 * (100 - sent_crew) + received
        print(score, expected)
    