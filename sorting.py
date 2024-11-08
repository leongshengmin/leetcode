from typing import List


def insertion_sort(arr:List):
    """
    assume all items <= idx i are sorted
    let i = largest of sorted (ie the pivot index)
    let j = i + 1
    compare j with i
        if j >= i --> leave it be
        if j < i --> move items between arr[j]..arr[i] by 1 to the right; increment i the pivot index
    """
    i = len(arr) - 1
    p = 0
    print(arr)
    while i > 0 and p < len(arr) and p < i:
        if arr[i] >= arr[p]:
            i-=1
            p=p+1
            continue
        
        # arr[i] < arr[p]
        j = i-1
        tmpi = arr[i]
        while j >= p:
            print(f"i={i}, setting arr[j+1] -> arr[j]: {arr[j+1]} -> {arr[j]}")
            arr[j+1] = arr[j]
            j=j-1
        
        arr[max(p-1, 0)] = tmpi
        print(f"i={i}, arr={arr}")
    
        i=i-1
    
    print(arr)

"""


my_array = [64, 34, 25, 12, 22, 11, 90, 5]

n = len(my_array)
for i in range(1,n):
    insert_index = i
    current_value = my_array.pop(i)
    for j in range(i-1, -1, -1):
        if my_array[j] > current_value:
            insert_index = j
    my_array.insert(insert_index, current_value)
"""

insertion_sort([3, 2, 4, 9, 2])
