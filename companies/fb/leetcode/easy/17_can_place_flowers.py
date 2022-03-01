'''
You have a long flowerbed in which some of the plots are planted, and some are not. However, flowers cannot be planted in adjacent plots.

Given an integer array flowerbed containing 0's and 1's, where 0 means empty and 1 means not empty, and an integer n, return if n new flowers can be planted in the flowerbed without violating the no-adjacent-flowers rule.

 

Example 1:

Input: flowerbed = [1,0,0,0,1], n = 1
Output: true
Example 2:

Input: flowerbed = [1,0,0,0,1], n = 2
Output: false
 

Constraints:

1 <= flowerbed.length <= 2 * 104
flowerbed[i] is 0 or 1.
There are no two adjacent flowers in flowerbed.
0 <= n <= flowerbed.length
'''

'''
Instead of using that super long 'if condition'. Its better to add 0 at the start and end of the list.
Makes it cleaner and easier to understand!
'''

class Solution:
    def canPlaceFlowers(self, flowerbed: List[int], n: int) -> bool:
        s = len(flowerbed)
        bed = [0] + flowerbed + [0]
        
        for i in range(1, s+1):
            if bed[i] == bed[i-1] == bed[i+1] == 0:
                bed[i] = 1
                n -= 1
            
            if n <= 0: return True
        
        return False
