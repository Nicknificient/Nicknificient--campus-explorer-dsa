from __future__ import annotations
from data_structures.array_list import ArrayList
from data_structures.referential_array import ArrayR, T
from typing import Callable, Any, TypeVar

# We are defining a type, and we are saying it can be either an ArrayList or an ArrayR.
ListOrArray = TypeVar("ListOrArray", ArrayList[T], ArrayR[T])


def bubble_sort(the_list: ListOrArray, key: Callable[[T], Any] = lambda x: x) -> None:
    """
    Sort an array or list using bubble sort.

    :complexity:
        Best case  O(N) when the list is mostly sorted
        Worst case O(N^2)
        Where N is the length of the list.
    """
    n = len(the_list)
    for mark in range(n-1,0,-1):
        swapped = False
        for i in range(mark):
            if key(the_list[i]) > key(the_list[i+1]):
                the_list[i], the_list[i+1] = the_list[i+1], the_list[i]
                swapped = True
        if not swapped:
            break