from __future__ import annotations
from island import Island
from data_structures.hash_table import LinearProbeTable
from data_structures.heap import MaxHeap

class Mode1Navigator:
    """
    Student-TODO: short paragraph as per https://edstem.org/au/courses/12108/lessons/42810/slides/294117
    """

    def __init__(self, islands: list[Island], crew: int) -> None:
        """
        Student-TODO: Best/Worst Case
        """
        self.crew_num = crew
        self.num_islands = len(islands)
        self.islands = islands
        self.store = LinearProbeTable([self.num_islands])
        self.store.hash = lambda x: int(x) % self.num_islands
        for island in islands:
            money_marine_r = island.money/island.marines
            self.store[money_marine_r] = island

    def select_islands(self) -> list[tuple[Island, int]]:
        """
        Student-TODO: Best/Worst Case
        """
        sorted_ratio = MaxHeap(self.num_islands)
        for island in self.islands:
            money_marine_r = island.money/island.marines
            sorted_ratio.add(money_marine_r)

        crew_available = self.crew_num
        res = []
        for _ in range(self.num_islands):
            curr_max = sorted_ratio.get_max()
            tar_island: Island = self.store[curr_max]
            crew_require = tar_island.marines
            if crew_available > crew_require:
                res.append((tar_island, crew_require))
                crew_available -= crew_require
            elif crew_available == 0:
                res.append((tar_island, 0))
            elif crew_available <= crew_require:
                res.append((tar_island, crew_available))
                crew_available = 0
        return res
    
    # def select_island_aux(final_list: list[tuple[Island, int]], crew_num: int): list[tuple[Island, int]]
        
    def select_islands_from_crew_numbers(self, crew_numbers: list[int]) -> list[float]:
        """
        Student-TODO: Best/Worst Case
        """
        sorted_ratio = MaxHeap(self.num_islands)
        for island in self.islands:
            money_marine_r = island.money/island.marines
            sorted_ratio.add(money_marine_r)
        
        island_key_list = []
        for _ in range(self.num_islands):
            island_key_list.append(sorted_ratio.get_max())
        
        res = []
        for crew_num in crew_numbers:
            max_value = 0
            crew_available = crew_num
            for i in range(self.num_islands):
                curr_max = island_key_list[i]
                tar_island: Island = self.store[curr_max]
                money = tar_island.money
                marine = tar_island.marines
                crew_require = tar_island.marines
                if crew_available > crew_require:
                    max_value += min(crew_available*money/marine, money)
                    crew_available -= crew_require
                elif crew_available == 0:
                    break
                elif crew_available <= crew_require:
                    max_value += min(crew_available*money/marine, money)
                    crew_available = 0
            res.append(max_value)
        return res     


    def update_island(self, island: Island, new_money: float, new_marines: int) -> None:
        """
        Student-TODO: Best/Worst Case
        """
        old_key = island.money/island.marines
        old_name = island.name
        updated_island:Island = Island(old_name, new_money, new_marines)
        updated_key = new_money/new_marines
        del self.store[old_key]
        self.store[updated_key] = updated_island

if __name__ == "__main__":

    # a = KeyStore("a", 12)
    # print(a.name)
    # f = lambda a: a.name
    # print(f(a))

    a = Island("A", 400, 100)
    b = Island("B", 300, 150)
    c = Island("C", 100, 5)
    d = Island("D", 350, 90)
    e = Island("E", 300, 100)
    islands: list = [a, b, c, d, e]
    crew_num = 200
    navi = Mode1Navigator(islands, crew_num)
    print(navi.select_islands())