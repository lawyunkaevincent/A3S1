from __future__ import annotations
from island import Island
from data_structures.hash_table import LinearProbeTable
from data_structures.heap import MaxHeap
from data_structures.bst import BinarySearchTree, BSTInOrderIterator

class Mode1Navigator:
    """
    Student-TODO: short paragraph as per https://edstem.org/au/courses/12108/lessons/42810/slides/294117
    """

    def __init__(self, islands: list[Island], crew: int) -> None:
        """
        Initialise the Nove1Navigator class with initial state of islands and number of crew
        that is taken on the journey

        :complexity: O(N), where N is the number of island in the argument list named 'islands'
        """
        self.crew_num = crew
        self.num_islands = len(islands)
        self.islands_l = islands
         # Create a BST to store all the island with key as the marine-money ratio
        self.bst_store = BinarySearchTree()
        # Add all the island into the binary search tree created with key as marine-money ratio of the island
        # and value is simply the island itself
        for island in islands:  # O(NlogN) -> depth of BST is bounded by logN
            marine_money_r = island.marines/island.money
            self.bst_store[marine_money_r] = island # setitem in BST has complexity O(logN), given the depth is bounded by logN

    def select_islands(self) -> list[tuple[Island, int]]:
        """
        Select the islands that we wish to attak and returning a list containing pairs, with each pair
        containing the island itself together with the number of crewmates that will be sent to each island

        :complexity: O(NlogN), where N is the number of islands

        :strategy: Create max heap - a for loop of N time - get max money-marine ratio - find respective island - allocate crew members accordingly
        """
        # Creat an inorder iterator to get the island according to the marine-money ratio in ascending order
        bst_iter = BSTInOrderIterator(self.bst_store.root)

        # while sending crewmates, island with lower marine-money ratio will be given priority to maximise the 
        # money make, thus in order traversal is used to traserve the bst_store in ascending order.
        crew_available = self.crew_num
        res = []
        for collection in bst_iter: # loop through all the node, O(N)
            tar_island: Island = collection.item   # _getitem_ for LinearProbeTable is expected to have O(1) complexity
            crew_require = tar_island.marines   # compute the crew required to get all the money on the island
            # has enough crewmates to get all the money on the island 
            if crew_available > crew_require:
                res.append((tar_island, crew_require))  # append method of a list has O(1) complexity 
                crew_available -= crew_require
            # no more crewmates available
            elif crew_available == 0:
                res.append((tar_island, 0))
            # crewmates available is not enough to pirates all the money on the island
            elif crew_available <= crew_require:
                res.append((tar_island, crew_available))
                crew_available = 0
        return res
    
        
    def select_islands_from_crew_numbers(self, crew_numbers: list[int]) -> list[float]:
        """
        Calculate the most money that can be made with different crew combinations and return a
        list containing amount of money that could be made with respective crew size given in the crew_numbers list

        :complexity: O(C*N)
        """
        res = []
        for crew_num in crew_numbers: # loop through different crew number in argument list 'crew_numbers' 
            max_value = 0
            crew_available = crew_num
            # Creat an inorder iterator to get the island according to the marine-money ratio in ascending order
            bst_iter = BSTInOrderIterator(self.bst_store.root)
            for collection in bst_iter:
                tar_island: Island = collection.item
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
        old_key = island.marines/island.money
        old_name = island.name
        updated_island:Island = Island(old_name, new_money, new_marines)
        updated_key = new_marines/new_money
        del self.bst_store[old_key]
        self.bst_store[updated_key] = updated_island

if __name__ == "__main__":
    a = Island("A", 400, 100)
    b = Island("B", 300, 150)
    c = Island("C", 100, 5)
    d = Island("D", 350, 90)
    e = Island("E", 300, 100)
    islands: list = [a, b, c, d, e]
    crew_num = 200
    navi = Mode1Navigator(islands, crew_num)
    print(navi.select_islands())