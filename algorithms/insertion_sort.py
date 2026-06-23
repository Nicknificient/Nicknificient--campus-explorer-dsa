from __future__ import annotations

from data_structures.array_list import ArrayList
from data_structures.referential_array import ArrayR, T
from typing import Callable, Any, TypeVar

# We are defining a type, and we are saying it can be either an ArrayList or an ArrayR.
ListOrArray = TypeVar("ListOrArray", ArrayList[T], ArrayR[T])


def insertion_sort(the_list: ListOrArray, key: Callable[[T], Any] = lambda x: x) -> None:
    """
    Sort an array or list using insertion sort.

    :complexity:
        Best case  O(N) when the list is mostly sorted
        Worst case O(N^2)
        Where N is the length of the list.
    """
    for i in range(1, len(the_list)):
        j = i - 1
        tmp = the_list[i]
        while j >= 0 and key(tmp) < key(the_list[j]):
            the_list[j + 1] = the_list[j]
            j -= 1

        the_list[j + 1] = tmp