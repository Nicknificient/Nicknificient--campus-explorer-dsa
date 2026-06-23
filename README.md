# Campus Explorer: Data Structures & Algorithms in Practice

A campus exploration simulation solved with hand-implemented data structures — no Python built-in `list`, `dict`, or `heapq`. Every traversal, search, and ranking operation runs on a custom Abstract Data Type chosen deliberately for the access pattern each task demands, with a formal best/worst-case time complexity proof for every method.

---

## Quick start

```bash
python exploration.py        # graph traversal: greedy walk + full path enumeration
python location_manager.py   # BST + hash table: range queries, top-k, dynamic updates
python reward_seeker.py      # max-heap: repeated highest-reward extraction
python leaderboard.py        # merge sort + stable two-leaderboard merge
```

Each file loads a real campus dataset ([`clayton.txt`](./clayton.txt) or [`malaysia.txt`](./malaysia.txt)) and runs its own inline assertions on exit. Sample output from `location_manager.py`:

```
>>> location_manager = LocationManager('clayton')
>>> location_manager.get_locations_in_range(1.5, 6.0)
[(2.2, 'Robert Blackwood Hall'), (3.5, 'Law Building and Library'),
 (3.6, 'Alan Finkel Building for Technology and Design'), ...,
 (6.0, 'Religious Centre')]

>>> location_manager.get_top_k_locations(3)
[(13.0, 'New Horizons'), (8.0, 'Monash Club'), (6.0, 'Religious Centre')]
```

---

## The problem space

Clayton and Malaysia campuses are each modelled as a directed graph: locations are nodes carrying a reward value, and connections between them carry a difficulty cost. Four subsystems sit on top of this graph, each with a genuinely different access pattern:

1. **Exploration** ([`exploration.py`](./exploration.py)) — a stamina-limited greedy walk, plus full recursive enumeration of every path through the graph (total difficulty, longest path / max reward).
2. **Location ranking** ([`location_manager.py`](./location_manager.py)) — query locations by a derived "desirability" score: range queries, top-k, and live reward updates.
3. **Reward seeking** ([`reward_seeker.py`](./reward_seeker.py), [`reward_structure.py`](./reward_structure.py)) — repeatedly extract the single highest-reward unvisited location, with mid-exploration reward updates.
4. **Leaderboard** ([`leaderboard.py`](./leaderboard.py)) — sort players by a composite key (score, then stamina), and merge two independently-sorted leaderboards in stable order.

All four touch "rank by value, query repeatedly, support updates" — but each is solved with the structure that fits its *specific* query shape, not the same default reused four times. That contrast is the point of this project.

---

## Why a different ADT for each task

| Task | ADT chosen | Why this one, not another |
|---|---|---|
| [`exploration.py`](./exploration.py) | Plain recursion over the graph — no auxiliary ADT | No index is needed when every traversal has to visit connections directly anyway. The greedy method picks the lowest-difficulty (tie-broken by reward) outgoing edge at each step; the two enumeration methods compute path-count/difficulty-sum and longest-path/max-reward in a single post-order pass each, rather than re-walking the graph per query. |
| [`location_manager.py`](./location_manager.py) | `BinarySearchTree` keyed by `(desirability, name)` + `HashTableSeparateChaining` for name lookup | Range queries and ordered top-k are exactly what a BST is for — an (reverse) in-order traversal returns results already sorted, no separate sort step needed. The hash table exists only to avoid an O(N) tree search whenever a location must be found *by name* for an update. |
| [`reward_seeker.py`](./reward_seeker.py) / [`reward_structure.py`](./reward_structure.py) | Custom `ArrayMaxHeap` subclass (`RewardMaxHeap`) + a position-tracking hash table | This task never needs a range or an ordered scan — only "the current maximum," repeatedly. A heap gives O(log N) extract-max, which is simpler and lower-overhead than a BST when ranges are never queried. The position-tracking hash table turns `update_reward` from an O(N) scan into an O(log N) direct rise/sink. |
| [`leaderboard.py`](./leaderboard.py) | `merge_sort` for the initial sort, a linear two-pointer merge for `combine()` | Both leaderboards are already sorted before combining, so re-sorting their union would throw away information already known. A single O(N+M) merge pass — the same idea `merge_sort` uses internally — exploits that the inputs are already ordered, which a generic sort can't. |

---

## Complexity analysis, with proof

Every public method carries a documented best/worst-case complexity derived from the structure actually used. Two representative examples:

**`LocationManager.get_top_k_locations(k)`** — a reverse in-order traversal (right → node → left) visits the highest-desirability locations first and stops as soon as `k` results are collected:

```python
def _top_k_helper(self, current, k, result):
    if current is None or len(result) == k:
        return
    self._top_k_helper(current.right, k, result)
    if len(result) < k:
        result.append((current.key[0], current.item.get_name()))
    if len(result) < k:
        self._top_k_helper(current.left, k, result)
```
**O(log N + K)** — not the O(N log N) a full extract-and-sort would cost, because the traversal stops the moment `k` results are in hand.

**`RewardSeeker.update_location_reward`** — updating a reward inside the max-heap isn't a simple overwrite; the heap invariant has to be restored. The position-tracking hash table means the location's array index is known in O(1), so the update calls `_rise` or `_sink` directly — **O(log N)**, instead of the O(N) it would take to first *find* the entry by scanning the array.

```
exploration.py — greedy_student(location, stamina)
Best case:  O(1)      — no outgoing connections, or stamina already 0
Worst case: O(S * D)  — S = stamina, D = max outgoing connections per location;
                         up to S steps, each scanning up to D connections
```

> **On the underlying assumptions:** proofs that depend on "BST operations are O(log N)" rely on an assumption stated by the unit — that the tree stays reasonably balanced for the data used. An adversarial insertion order could degrade an *unbalanced* BST to O(N) per operation; that trade-off (simplicity vs. guaranteed balance, e.g. AVL/red-black) is a deliberate scope boundary of the assignment, stated here rather than glossed over.

---

## Repository structure

```
campus_explorer/
├── exploration.py          graph traversal: greedy stamina walk, path enumeration
├── location_manager.py     BST + hash table: range queries, top-k, dynamic updates
├── reward_seeker.py        max-heap-backed repeated highest-reward extraction
├── reward_structure.py     RewardEntry, RewardStatus, RewardMaxHeap (heap + position index)
├── leaderboard.py          merge sort + stable two-leaderboard merge
├── algorithms/             provided: bubble, insertion, merge, quick, selection sort
├── data_structures/        provided: ArrayList, BST, hash table, heap, linked structures
├── clayton.txt             campus graph + leaderboard data, Clayton
├── malaysia.txt            campus graph + leaderboard data, Malaysia
└── campus.py               provided: campus/location/connection/leaderboard loader
```

`algorithms/` and `data_structures/` were supplied by the unit as the only permitted building blocks — no Python built-in `list`, `dict`, `set`, or `heapq` appears anywhere in the five files above; every container operation goes through one of these custom ADTs.

---

## Skills Demonstrated

Matching the right ADT to an access pattern rather than defaulting to a familiar one; formal best/worst-case complexity analysis grounded in the structure actually used; building on hand-rolled data structures without language built-ins; and being explicit about the practical trade-offs (e.g. balanced vs. unbalanced trees) that complexity claims depend on.
