from __future__ import annotations
from data_structures.array_list import ArrayList
from data_structures.referential_array import ArrayR, T
from typing import TypeVar

# We are defining a type, and we are saying it can be either an ArrayList or an ArrayR.
ListOrArray = TypeVar("ListOrArray", ArrayList[T], ArrayR[T])


def quick_sort(the_list: ListOrArray, key=lambda x: x) -> None:
    """
    Quick sorts two list in place.
    The `key` kwarg allows you to define a custom sorting order.

    :complexity:
        Best case  O(NlogN) - Equal sub divisions of the lists
        Worst case O(N^2) - Only reducing list by 1 element each iteration
        Where N is the length of the list.
    """
    def quick_sort_aux(the_list: ListOrArray, start: int, end: int, key=lambda x: x) -> None:
        if start < end:
            boundary = partition(the_list, start, end, key)
            quick_sort_aux(the_list, start, boundary - 1, key)
            quick_sort_aux(the_list, boundary + 1, end, key)

    def partition(the_list: ListOrArray, start: int, end: int, key=lambda x: x) -> int:
        mid = (start + end) // 2
        pivot = the_list[mid]
        the_list[start], the_list[mid] = the_list[mid], the_list[start]
        boundary = start

        for k in range(start + 1, end + 1):
            if key(the_list[k]) < key(pivot):
                boundary += 1
                the_list[k], the_list[boundary] = the_list[boundary], the_list[k]
        the_list[start], the_list[boundary] = the_list[boundary], the_list[start]

        return boundary

    start = 0
    end = len(the_list)-1
    quick_sort_aux(the_list, start, end, key)