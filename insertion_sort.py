from typing import List

"""
Insertion sort is a simple sorting algorithm that works by iteratively inserting each element of an unsorted list into its correct position in a sorted portion of the list. It is like sorting playing cards in your hands. You split the cards into two groups: the sorted cards and the unsorted cards. Then, you pick a card from the unsorted group and put it in the right place in the sorted group.

    We start with second element of the array as first element in the array is assumed to be sorted.
    Compare second element with the first element and check if the second element is smaller then swap them.
    Move to the third element and compare it with the first two elements and put at its correct position
    Repeat until the entire array is sorted.

# Python program for implementation of Insertion Sort

# Function to sort array using insertion sort
def insertionSort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        # Move elements of arr[0..i-1], that are
        # greater than key, to one position ahead
        # of their current position
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

# A utility function to print array of size n
def printArray(arr):
    for i in range(len(arr)):
        print(arr[i], end=" ")
    print()

# Driver method
if __name__ == "__main__":
    arr = [12, 11, 13, 5, 6]
    insertionSort(arr)
    printArray(arr)
"""


def insertionSort(arr: List):
    pass


# Driver method
if __name__ == "__main__":
    arr = [12, 11, 13, 5, 6]
    insertionSort(arr)
