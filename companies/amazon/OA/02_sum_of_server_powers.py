'''
You are given an input integer array of n-length.

Sum, for all subarrays:
Minimum in subarray * Sum of subarray.

For instance:
[1,3,4]

min(1) * sum(1) = 1 * 1 =            1
min(1,3) * sum(1,3) = 1 * 4 =        4
min(1,3,4) * sum(1,3,4) = 1 * 8 =    8
min(3) * sum(3) = 3 * 3 =            9
min(3,4) * sum(3,4) = 3 * 7 =        21
min(4) * sum(4) =4 * 4 =             16
1+4+8+9+21+16 =                      59
for a returned value of 59

I could not find an equivalent question on leetcode.

# LOGIC ?
For my solution, I made an array of the sums of subarrays by going backwards and summing the values. Using the example above, it would be:
[8,7,4]
Then if I needed to find the sum of subarray in index 1 to 2, I'd do sumSubArray[1] - sumSubArray[2] 
(if the right index is >= the last index of the array, I don't subtract anything.)

##################################################################################################################
Given an array find sum of scores of all possible subarrays of the array.
Score of a subarray = product of min element and sum of elements in the subarray 
Max Size of array  = 8*10^5

# LOGIC
What I did in actual test was 
Get all subarrays by varying Li, Ri (2 loops)
Get sum b/w Li , Ri using prefix sum
And then get min b/w Li, Ri using segment tree min queries

1. Prefix sum pre calculation was O(n)
2. Creating segment tree O(nlogn)
3. Looping was n square
4. Inside loop for each subarray getting sum in O(1), getting min in O(logn) using segment tree querying.

Overall O(n square log n)
We need a solution with complexity less than O(n^2)
'''

##################################################################################################################
# SOLUTION IDEA - 1:

'''
I got the same question in amazon OA and could not solve it. But the trick here is, you need to find all the subarrays (and get min of each subarray, also sum of each subarray) and multiply them and add the multiplied results.

here is the explanation for your input array [1, 3, 4]
Total subarrays you can form using this is [1], [3], [1, 3], [1, 3, 4], [3, 4], [4].

Now min of each of this subarray is minSubarray = [1, 3, 1, 1, 3, 4]
Also, sum of each subbaray is sumSubarray = [1, 3, 4, 8, 7, 4]

now multiply these, [11, 33, 14, 18, 37, 44] will be [1, 9, 4, 8, 21, 16].
if you sum these you will get 59 (1+9+4+8+21+16)

Hope this helps..

Similar question:
https://leetcode.com/problems/sum-of-subarray-minimums/
https://leetcode.com/discuss/interview-question/1736639/Solution-to-Amazon-OA-2022-problem-Sum-of-Scores-of-Subarray

It is different, but similar I think.
https://leetcode.com/problems/sum-of-subsequence-widths/
'''

####################################################################################################################
# SOLUTION - 2
# https://leetcode.com/playground/m9BXwSBc
# There are actually multiple post with the same problem. I have commented this same solution there. 
# https://leetcode.com/discuss/interview-question/1706805/Amazon-OA-Question-Is-there-an-O(n) 
# https://leetcode.com/discuss/interview-question/1711676/How-to-solve-this-contest-question

def optimalScoresOfSubArrays(arr):
    prefixSums = []
    positionElementProdSums = []
    positionElementProdSumsReverse = []
    runningSum = 0
    posElementProdSum = 0
    n = len(arr)
    for i in range(n):
        runningSum += arr[i]
        posElementProdSum += (i+1) * arr[i]
        prefixSums.append(runningSum)
        positionElementProdSums.append(posElementProdSum)
    posElementProdSum = 0
    for i in range(n-1,-1,-1):
        posElementProdSum += (n-i) * arr[i]
        positionElementProdSumsReverse.append(posElementProdSum)
        
    sum = lambda sums, l, r: sums[r] - (sums[l-1] if l-1>=0 else 0) if l <= r else 0
    totalScore = 0
    stack = []
    for i in range(n):
        while stack and arr[stack[-1][0]] > arr[i]:
            minElementIndex, leftIndex = stack.pop()
            rightIndex = i
            rightCount = rightIndex - minElementIndex
            leftCount = minElementIndex - leftIndex
            minElement = arr[minElementIndex]
            shiftedPosEleProdSum = sum(positionElementProdSums, leftIndex + 1, minElementIndex) - sum(prefixSums, leftIndex  + 1, minElementIndex) * (leftIndex  + 1)
            currRangeScore = rightCount * minElement * shiftedPosEleProdSum
            totalScore += currRangeScore
            shiftedPosEleProdSum = sum(positionElementProdSumsReverse, n-rightIndex, n-minElementIndex-2) - sum(prefixSums, minElementIndex+1, rightIndex-1)*(n-rightIndex)
            currRangeScore = leftCount * minElement * shiftedPosEleProdSum
            totalScore += currRangeScore
        if not stack: stack.append((i, -1))
        else: stack.append((i, stack[-1][0]))
    while stack:
        minElementIndex, leftIndex = stack.pop()
        rightIndex = n
        rightCount = rightIndex - minElementIndex
        leftCount = minElementIndex - leftIndex
        minElement = arr[minElementIndex]
        shiftedPosEleProdSum = sum(positionElementProdSums, leftIndex + 1, minElementIndex) - sum(prefixSums, leftIndex  + 1, minElementIndex) * (leftIndex  + 1)
        currRangeScore = rightCount * minElement * shiftedPosEleProdSum
        totalScore += currRangeScore
        shiftedPosEleProdSum = sum(positionElementProdSumsReverse, n-rightIndex, n-minElementIndex-2) - sum(prefixSums, minElementIndex+1, rightIndex-1)*(n-rightIndex)
        currRangeScore = leftCount * minElement * shiftedPosEleProdSum
        totalScore += currRangeScore
    return totalScore
  
def bruteForceScoresOfSubArrays(arr):
    totalScore = 0
    n = len(arr)
    for i in range(n):
        minEle = float('inf')
        sum = 0
        for j  in range(i, n):
            sum += arr[j]
            minEle = min(minEle, arr[j])
            totalScore += sum * minEle
    return totalScore


arr =[529,7655,4113,7929,7745,6149,2691,435,7858,978,5467,8761,2881,4175,359,9711,7157,1740,5214,7660,1113,614,4077,2859,2954,1170,3997,4526,2771,4046,3174,7126,3866,7603,5596,9587,1826,9228,9983,2487,7018,1130,1299,1389,5914,2926,5679,5781,5770,8705,9053,3449,9893,6042,4349,2008,2959,9730,5639,8813,5206,747,460,149,2553,4006,2012,8966,2245,2635,9089,7962,5879,9785,1069,7122,7926,9546,4557,5719,6926,2353,1887,2744,2240,472,7559,824,4320,8267,7210,4764,8368,3071,8973,7849,8704,2375,5130,5092,8311,6147,7692,6794,8280,4863,4932,4863,946,4243,7307,5061,3752,426,6352,1978,818,5604,3306,9034,9805,7900,8462,4473,1914,8449,113,8566,7671,9518,693,730,8064,2004,9584,8725,4392,468,3013,502,6472,4185,6380,471,4258,3424,8435,7470,5109,7228,486,8925,3130,1574,4454,9048,5824,679,5364,3804,5143,6714,5695,2806,7653,9153,26,3195,2856,4303,6914,270,9011,3325,7835,1770,8668,3395,1756,6702,743,2618,6841,7492,6068,9150,8852,5004,9610,6716,7053,4937,6209,2772,4454,3988,432,8097,9400,3194,5565,6266,2821,4769,5019,164,443,8620,695,8173,7705,5081,1376,6573,9364,7328,2513,8020,2361,4915,5346,7410,2379,5538,7560,9431,1049,9069,9616,9368,3998,3240,8006,3177,4380,794,8668,4685,3456,2257,2645,7269,2424,5209,4198,3086,6821,7598,3764,7505,6191,9018,7019,338,5606,1484,1962,1415,8423,6988,9140,8305,6196,2299,3397,8634,3855,2139,4924,7102,4662,6713,1056,5418,5982,940,3149,9245,637,8873,7651,2975,6447,5539,291,9119,7773,9287,4286,858,9111,5012,9499,1595,4408,918,5742,5134,9475,8427,9556,8422,4825,9747,522,266,9267,7351,5413,7374,8556,8014,6194,6076,3011,1612,217,6101,7673,5623,6757,5038,2615,3711,8296,7453,408,868,4090,1038,6549,7307,7886,3571,6450,1947,5236,8943,5827,1325,1278,9292,1930,7778,6039,3935,623,7886,256,1194,833,4219,3641,1047,2543,4442,9242,150,8148,1460,9650,5882,9647,431,7709,714,6345,6104,3240,6151,6310,7220,216,6452,3271,3368,1247,7870,8492,2124,1932,3524,5515,2911,8798,7242,1019,8154,3942,5654,5994,8323,449,1914,5680,2821,8399,1904,6356,8538,298,7418,2339,1672,2948,584,4877,2702,36,8044,1528,3815,799,8865,7043,5846,3204,4238,3012,2060,8169,9422,8049,8871,1517,819,6066,4821,7262,6131,9774,9210,9683,338,3573,3812,4398,5022,1313,9705,792,3644,3397,529,8340,2683,524,5635,6653,9852,8619,39,6060,4273,3026,7680,6861,4470,8,4094,4720,388,9344,7749,394,3603,8406,8713,9328,4423,3074,9966,694,4094,3627,6926,3558,4322,1720,3814,7277,5770,7077,9871,7872,4016,1196,7425,8843,8631,2500,142,991,9472,1603,7433,2955,5213,3083,9960,3993,8940,2675,5442,8308,6653,2105,4640,2020,8924,8918,2949,4949,5442,9580,2811,5205,7078,9779,5049,4455,3420,5586,6315,1629,101,5384,4917,7629,2731,8121,2852,9260,8445,2896,8075,4667,2164,7085,3616,3177,9104,5318,8728,2332,3943,2388,4352,8537,199,1655,3881,7058,3912,7027,5721,9737,6031,3265,2699,8285,7835]
print("Brute Force:", bruteForceScoresOfSubArrays(arr))
print("Optimal:", optimalScoresOfSubArrays(arr))
