from __future__ import annotations
from dataclasses import dataclass
from island import Island
from data_structures.heap import MaxHeap

class Mode2Navigator:
    """
    The data structure used for this class is in-built dictionary and MaxHeap
    """

    def __init__(self, n_pirates: int) -> None:
        """
        Initialise the Mode2 NaviGator Class

        :param args:
            n_pirates: number of pirates involved in the Davy Back Fight
        
        :complexity: O(1)

        :further explanation: 
            The initialisation method has constant time complexity because it only involve
            constant time operations which is simple assignment and creation of a dictionary.
        """
        self.n_pirates = n_pirates
        # Create a dictionary to store the island on the sea using the island name as the key
        self.island_dict: dict[str,Island] = {}
        
    def add_islands(self, islands: list[Island]):
        """
        Add islands to the seas.

        :param args:
            islands: a list of Island instances to be added to the sea

        :complexity: O(I) where I is the length of 'islands' list 

        :further explanation:
            This method simply loop through the 'islands' list and add all the Island instance
            in the list to the instance variable self.island_dict dictionary. __setitem__ method
            in python in-built dictionary is assumed to have complexity of O(1), thus the complexity
            of this method depends simply on the number of island in the parameter arguments 'islands' list.
        """
        for island in islands:
            self.island_dict[island.name] = island

    def simulate_day(self, crew: int) -> list[tuple[Island|None, int]]:
        """
        Simulate a day of Davy Back Fight and return a list of tuples, representing
        the choices made by the first, second, ... captain in order. Each tuple contain the
        island that was plundered and number of crews that were sent onto the island

        :param args: 
            crew: Size of the crew for every pirate captain
        
        :best case: happens when all the island has mmratio <= 2
        :worst case: happens when all the island has mmratio > 2
        """
        # create a list to store the plundered island and number of crew sent to the island
        island_crew_l: list[tuple[Island|None, int]] = []
        crew_available = crew
        # create a heap to store the score that the pirate will get for each island that have money-marine ratio greater than 2
        # If money-marine ratio <= 2, no plundering will result in higher score, thus whenever an island have money-marine ratio <= 2, 
        # it is not stored into the score heap
        score_heap = MaxHeap(len(self.island_dict))

        # create a list named 'island_score_l' and append all the island and score into the list for heapifying 
        island_score_l = []
        # O(N)
        for island in self.island_dict.values():
            marine = island.marines
            money = island.money
            crew_left = crew_available-marine
            try:
                if money/marine > 2:
                    score = money/marine*min(crew_available,marine)+2*max(0, crew_left)
                    # compute the sorted key for MaxHeap using HeapKey class, which is an auxiliary class to store information for both
                    # scores and island name in the key
                    key = HeapKey(island.name, score)
                    island_score_l.append(key)   # append in python list take O(1) complexity
            except ZeroDivisionError:   # handle situation for an island with zero marine left after being looped by one round
                continue
           
        # O(N)
        # Heapifying the island score list
        score_heap = score_heap.heapify(island_score_l)

        # O(C*log(N))
        for _ in range(self.n_pirates):
            # still have island that can be plundered to make higher score
            if len(score_heap) != 0:
                # get the island name and score pair stored in HeapKey class
                tar_heapkey:HeapKey = score_heap.get_max()  # O(logN)
                # get the corresponding island name
                island_name = tar_heapkey.name
                tar_island: Island = self.island_dict[island_name]
                marine = tar_island.marines
                money = tar_island.money
                crew_left = crew_available-marine   # marine is the crew required to loot the whole island
                # have enough crew to loot the whole island (other crew wont come back and loot this island since its resources is completely loop)
                if crew_left >= 0:
                    updated_island = Island(tar_island.name, 0, 0)
                    self.island_dict[tar_island.name] = updated_island  # update island state in the island_dict
                    island_crew_l.append((updated_island, marine))
                # not enough crew to loot the whole island (the island can still be looted by other crew )
                else:
                    money_plundered = crew_available*money/marine
                    marine_left = marine - crew_available
                    money_left = money-money_plundered
                    updated_island = Island(tar_island.name, money_left, marine_left)
                    island_crew_l.append((updated_island, crew_available))
                    self.island_dict[island_name] = updated_island
                    # recompute the updated key and add it into the heap
                    updated_crew_left = crew_available-marine_left  # compute crew-left if other pirate loot this island again
                    updated_score = money_left/marine_left*min(crew_available,marine_left)+2*max(0, updated_crew_left)
                    updated_key = HeapKey(tar_island.name, updated_score)
                    # reappend the island score pair into the score_heap
                    score_heap.add(updated_key)     # O(logN)

            # no plundering will make higher score
            else:
                island_crew_l.append((None, 0))
        return island_crew_l



@dataclass
class HeapKey:
    """
    An auxilliary class that is use to creat sorted key for the MaxHeap. In details, the sorted key created by HeapKey class
    will carry two information namely the island name and the score obtained if the pirate plunder the corresponding island.
    Since for Mode2Navigator class, only the name is unique for every island (can simply use money-marine ratio since two island might have the same ratio)
    , thus the name is used to create the key for instance variable island_dict in the class, 
    therefore in order to keep track of the island while computing the score obtained after plundering it,
    this class is created to to store both information. All the method of this class has complexity of O(1).
    """
    name: str
    score: float

    def __ge__(a: HeapKey, b: HeapKey):
        """
        Magic method greater than equal
        Compare two KeyStore based on their moneymarine ratio

        :complexity: O(1), all the operations are of constant time
        """
        return (a.score >= b.score)
    
    def __gt__(a: HeapKey, b: HeapKey):
        """
        Magic method greater than
        Compare two KeyStore based on their moneymarine ratio

        :complexity: O(1), all the operations are of constant time
        """
        return (a.score > b.score)
        
    def __le__(a: HeapKey, b: HeapKey):
        """
        Magic method less than equal
        Compare two KeyStore based on their moneymarine ratio

        :complexity: O(1), all the operations are of constant time
        """
        return (a.score <= b.score)
    
    # def __lt__(a: HeapKey, b: HeapKey):
    #     """
    #     Magic method less than
    #     Compare two KeyStore based on their moneymarine ratio

    #     :complexity: O(1), all the operations are of constant time
    #     """
    #     return (a.score < b.score)
    
if __name__ == "__main__":
    a = Island("A", 400, 100)
    b = Island("B", 300, 150)
    c = Island("C", 100, 5)
    d = Island("D", 350, 90)
    e = Island("E", 300, 100)
    islands: list = [a, b, c, d, e]
    nav = Mode2Navigator(8)
    nav.add_islands(islands)
    print(nav.island_dict)
    results = nav.simulate_day(100)
    print(results)
    print(nav.island_dict)

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
    