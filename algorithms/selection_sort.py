from __future__ import annotations

from data_structures.array_list import ArrayList
from data_structures.referential_array import ArrayR, T
from typing import Callable, Any, TypeVar

# We are defining a type, and we are saying it can be either an ArrayList or an ArrayR.
ListOrArray = TypeVar("ListOrArray", ArrayList[T], ArrayR[T])


def selection_sort(the_list: ListOrArray, key: Callable[[T], Any] = lambda x: x) -> None:
    """
    Sort an array or list using selection sort.

    :complexity:
        Best case  O(N^2)
        Worst case O(N^2)
        Where N is the length of the list.
    """
    n = len(the_list)
    for mark in range(n-1):
        pos_min = mark
        for i in range(mark + 1, n):
            if key(the_list[i]) < key(the_list[pos_min]):
                pos_min = i
        the_list[mark], the_list[pos_min] = the_list[pos_min], the_list[mark]