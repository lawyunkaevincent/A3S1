from __future__ import annotations
from island import Island
from data_structures.bst import BinarySearchTree

class Mode1Navigator:
    """
    The data structures used for this class is BinarySearchTree. 
    The depth of BST is assumed to be bounded by logN, where N is the number of nodes for this class.
    Strategy: 
        __init__ method:
            1. Initialise the crew number
            2. Add all the island into the BST named 'bst_store' with key as marine-money ratio and item as the island itself
            Note that this is viable due to the assumption that every island has different marine-money ratio. Also, the lower
            marine-money ratio of the island, the higher the amount of money can be looted at the island given the same amount 
            of crew. Thus for the following method, while assigning crew members to each island, priority is given to the island
            with lower marine-money ratio.
        select_islands method:
            1. Use a for loop to perform inorder traversal for the bst_store (Note that the default iterator given in the bst class
            iterate through the bst with inorder manner: left subtree, current node, right subtree) Inorder traversal will traverse through
            all the island which is stored in the bst_store according to their marine-money ratio in ascending order
            2. In the for loop, extract the information (marine numbers) of current island given by bst_store iterator.
            3. Allocate crew to the island according to the marine numbers and crew available.
            4. Append the tuple pair of island and crew number allocated into the final return list named 'island_crew_l'
            5. Repeat the process until the for loop ends.
        select_islands_from_crew_numbers method:
            1. Use a for loop to loop through all the crew number given in the 'crew_numbers' list
            2. For a single crew number, start by creating a variable named 'money_looted' to store the amount of money pirated
               by the crew.
            3. Use a for loop perform inorder traversal for bst_store and for extract informations(money and marine) for each island
               stored within. Compute and accumulate the amount of money pirated while sending crew to each island. Stop the iteration
               pirated through all the island or there is no more crew to be sent to pirate the island.
            4. Store the amount of money pirated into the return list named 'pirated_money_l'.
            5. Repeat the process for all the crew number in the crew_numbers list
        update_island method:
            Note that the marine-money ratio is used as key to store the island in the bst_store.
            1. Compute the old key used to store the island in the bst_store.
            2. Create a updated Island instance using the old_name of the island and the updated state
               given as parameters.
            3. Compute the updated key used to store the island in the bst_store using the new_money and new_marines.
            4. Delete the outdated island from the bst_store using old key
            5. Add the updated island into the bst_store using the updated key.
    """

    def __init__(self, islands: list[Island], crew: int) -> None:
        """
        Initialise the Nove1Navigator class with initial state of islands and number of crew
        that is taken on the journey

        :param args:
            : islands: number of islands on the sea to be navitaged
            : crew: number of crew that is taken on the journey

        :complexity: O(NlogN), where N is the number of island in the argument list named 'islands'

        :further explanation: 
            The complexity of the __init__ method depends on the for loop block when island is added into the Binary Search Tree named 'bst_store'.
            In details, __setitem__ method for BST has complexity of O(logN*compK), where N is the number of nodes in the BST and in this method
            can be interpreted as number of island and compK is the comparison costs for the key of the node which has O(1) complexity in this case 
            since the key is money-marine ratio which is a float, giving __setitem__ a final complexity of O(logN).
            The for loop itself is repeated for N times, thus resulting in O(NlogN) time complexity. All other operations in this method which
            involve assignment and initialisation of BST has O(1) complexity. Thus the overall dominating complexity is O(NlogN) for both best case and worst case. 
        """
        self.crew_num = crew
        self.num_islands = len(islands)
         # Create a BST 'bst_store' to store all the islands with key as the marine-money ratio
        self.bst_store = BinarySearchTree()
        # Add all islands into bst_store with key as marine-money ratio of the island value as the island itself
        # O(NlogN) -> depth of BST is bounded by logN, where N is the number of islands
        for island in islands:  
            marine_money_r = island.marines/island.money    # compute marine-money ratio
            self.bst_store[marine_money_r] = island # setitem in BST has complexity O(logN), given the depth is bounded by logN

    def select_islands(self) -> list[tuple[Island, int]]:
        """
        Select the islands that we wish to attack and returning a list containing pairs, with each pair
        containing the island itself together with the number of crew that will be sent to each island

        :complexity: O(N), where N is the number of island stored in the bst_store

        :further explanation: 
        """
        # while sending crewmates, island with lower marine-money ratio will be given priority to maximise the 
        # money make, thus in order traversal is used to traserve the bst_store in ascending order.
        crew_available = self.crew_num
        island_crew_l = []
        for ratio_island_pair in self.bst_store: # loop through all the node, O(N)
            tar_island: Island = ratio_island_pair.item   # O(1), extract item from the bst node
            crew_require = tar_island.marines   # compute the crew required to get all the money on the island
            # has enough crew to get all the money on the island 
            if crew_available > crew_require:
                island_crew_l.append((tar_island, crew_require))  # append method of a list has O(1) complexity 
                crew_available -= crew_require
            # no more crew available
            elif crew_available == 0:
                island_crew_l.append((tar_island, 0))
            # crew available is just enough or not enough to pirate all the money on the island
            elif crew_available <= crew_require:
                island_crew_l.append((tar_island, crew_available))
                crew_available = 0
        return island_crew_l
    
        
    def select_islands_from_crew_numbers(self, crew_numbers: list[int]) -> list[float]:
        """
        Calculate the most money that can be made with different crew combinations and return a
        list containing amount of money that could be made with respective crew size given in the crew_numbers list

        :param_args:
            crew_numbers: a list of crew number that is used to calculate the most money made if the amount is sent to pirate the islands

        :complexity: O(C*N), where C is the length of crew_numbers list and N is the number of islands in bst_store (created during initialisation)

        :further explanation: 
            The complexity of this method is governed by the nested for loop block. At the first layer of the nested for loop, all
            crew number given in the crew_numbers list is looped through to compute the maximum money pirated by the corresponding crew
            number. And within the first layer loop, there is a second layer loop to traverse through the bst_store to compute the amount
            of money that can be pirated from each islands. Within the second layer for loop, all the code has O(1) complexity since they
            only involve comparison of numbers, arithmetic operations and simple assignments. Thus, the final complexity of this method is 
            O(C*N), where C is the length of crew_numbers list and N is the number of islands given in 'islands' list during initialisation
            for both best case and worst case.
        """
        pirated_money_l = []
        for crew_num in crew_numbers: # loop through different crew number in argument list 'crew_numbers' 
            money_looted = 0  
            crew_available = crew_num
            for ratio_island_pair in self.bst_store:
                tar_island: Island = ratio_island_pair.item
                money = tar_island.money
                marine = tar_island.marines
                crew_require = tar_island.marines
                # manage to loot all the money on the islands
                if crew_available > crew_require:
                    money_looted += money
                    crew_available -= crew_require
                # no more crew available to loot money on islands remaining, break the loop
                elif crew_available == 0:
                    break
                # crew available is not enough to loot all the money on the island
                elif crew_available <= crew_require:
                    money_looted += crew_available*money/marine
                    crew_available = 0
            pirated_money_l.append(money_looted)    # append for list give O(1) complexity
        return pirated_money_l     


    def update_island(self, island: Island, new_money: float, new_marines: int) -> None:
        """
        Update the money or marine value of an island

        param args:
            island: Island instance to be updated
            new_money: value of money after updated
            new_marines: value of marines after updated

        complexity: 
            O(log(N)), where N is the number of island in the bst_store (created during initialisation)

        :further explanation:
            In this method, the complexity is governed by both __setitem__ and __delitem__ method of bst_store, 
            which have O(logN*compK), where N is the number of islands stored in the bst using marine-money ratio, 
            and compK is the comparison cost of the key which in this case, is O(1) since the keys (marine-money ratio)
            are float. All other codes has O(1) which involve arithmetic operations, simple assignment and createion of 
            new Island instance has complexity O(1). Thus the final complexity is O(constant + logN + logN) = O(2logN) = O(logN)
            for both best case and worst case. 
        """
        old_key = island.marines/island.money   
        old_name = island.name
        updated_island:Island = Island(old_name, new_money, new_marines)    # O(1): create an updated instance of island
        updated_key = new_marines/new_money # create an updated key of the updated island in the bst_store
        del self.bst_store[old_key] # O(logN)
        self.bst_store[updated_key] = updated_island   # O(logN)

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