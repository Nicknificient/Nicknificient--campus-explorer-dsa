# Campus Explorer: Data Structures & Algorithms in Practice

A campus exploration simulation built to demonstrate algorithmic problem-solving with hand-implemented data structures — no Python built-in `list`, `dict`, or `heapq` shortcuts. Every traversal, search, and ranking operation here is built on custom Abstract Data Types (ADTs) chosen deliberately for the access pattern each task demands, with formal best/worst-case time complexity analysis for every method.


---

## The problem space

Clayton and Malaysia campuses are each modelled as a directed graph: locations (buildings) are nodes, with a reward value attached to each, and connections between them carry a difficulty cost. On top of this graph sit three independent subsystems, each with a different access pattern, which is exactly why this project is interesting from a data-structures standpoint:

1. **Exploration** — a student with limited stamina greedily moves through campus, and separately, the system needs to analyse *all* possible paths through the graph (total difficulty across every complete path, and the highest-reward longest path).
2. **Location ranking** — locations need to be queried by a derived "desirability" score (reward relative to average outgoing difficulty), supporting range queries, top-k lookups, and reward updates — fast, and repeatedly.
3. **Reward seeking** — a different access pattern on the same idea: instead of *range* queries, this subsystem only ever needs "give me the single highest-reward unvisited location, repeatedly," with the ability to update a reward mid-exploration.
4. **Leaderboard** — player scores from both campuses need to be sorted by a composite key (score, then stamina) and two independently-sorted leaderboards need to be combined into one, in a stable order.

Four problems that all touch "rank by value, query repeatedly, support updates" — but each is solved with the data structure that actually fits the *shape* of its query pattern, not the same hammer reused four times. That contrast is the core of what this project demonstrates.

---

## Why a different ADT for each task

| Task | ADT chosen | Why this one, not another |
|---|---|---|
| **Exploration** (`exploration.py`) | Plain recursion over the graph (no auxiliary ADT) | The graph is already the right structure — no index is needed when every traversal has to visit connections directly. A greedy method picks the lowest-difficulty (tie-broken by reward) outgoing edge at each step; two further methods perform full recursive enumeration to compute path-count/difficulty-sum and longest-path/max-reward in a single post-order pass each, rather than re-walking the graph per query. |
| **Location ranking** (`location_manager.py`) | `BinarySearchTree` keyed by `(desirability, name)`, backed by a `HashTableSeparateChaining` for name lookup | Range queries and ordered top-k retrieval are exactly what a BST is for — an in-order (or reverse in-order) traversal naturally returns results in sorted order without a separate sort step. The hash table exists purely to avoid an O(N) tree search every time a location needs to be found *by name* for an update — two structures, each used for the query it's actually good at. |
| **Reward seeking** (`reward_seeker.py`, `reward_structure.py`) | A custom `ArrayMaxHeap` subclass (`RewardMaxHeap`) with a position-tracking hash table | This task never needs a *range* or an ordered scan — it only ever needs "the current maximum," repeatedly, with updates. A heap gives O(log N) extract-max and O(log N) updates, which a BST would also give, but a heap is the conceptually simpler and lower-overhead structure when ranges are never queried. The position-tracking hash table is what makes in-place reward updates (`update_reward`) possible in O(log N) instead of O(N) — without it, finding *where* a location sits in the heap array would require a linear scan. |
| **Leaderboard** (`leaderboard.py`) | `merge_sort` for the initial sort, a linear two-pointer merge for `combine()` | Both leaderboards are independently sorted before they're combined, so re-sorting the union from scratch would throw away information already known. A single O(N+M) merge pass — the same idea `merge_sort` uses internally to combine two sorted halves — exploits that the inputs are already ordered, which a generic sort can't do. |

---

## Complexity analysis

Every public method in this project carries a documented best-case and worst-case time complexity, derived from the actual structure used — not copied from a textbook. Two examples that show the reasoning style used throughout:

**`LocationManager.get_top_k_locations(k)`** — locations are stored in a BST ordered by desirability. Rather than extracting all N locations and sorting, a **reverse in-order traversal** (right → node → left) visits the highest-desirability locations first and stops as soon as `k` results are collected:

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
This gives **O(log N + K)** rather than the O(N log N) a full extract-and-sort would cost — the traversal does no more work than it has to once `k` results are in hand.

**`RewardSeeker.update_location_reward`** — updating a reward for a location already inside the max-heap is *not* a simple value overwrite, because the heap's ordering invariant has to be restored. The position-tracking hash table (`self.positions` inside `RewardMaxHeap`) means the location's array index is known in O(1), so the update can directly call `_rise` or `_sink` depending on whether the new reward is larger or smaller than its parent — **O(log N)** instead of the O(N) it would take to first *find* the entry by scanning the heap array.

A worked best/worst-case split (from `exploration.py`'s `greedy_student`):
```
Best case: O(1)
  — the starting location has no outgoing connections, or stamina is already 0.
Worst case: O(S * D)
  — S = stamina, D = max outgoing connections from any location.
  The student takes up to S steps, and at each step scans up to D
  outgoing connections to choose the next move.
```

> **A note on the underlying assumptions:** several of the complexity proofs above (e.g. "BST operations are O(log N)") rely on an assumption stated by the unit — that the binary search tree stays reasonably balanced for the data used. A real-world adversarial insertion order could degrade an *unbalanced* BST to O(N) per operation; that trade-off (simplicity vs. guaranteed balance, e.g. an AVL or red-black tree) is a deliberate scope boundary of the assignment, not an oversight, and is worth being explicit about rather than overstating the guarantee.

---

## Repository structure

```
campus_explorer/
├── exploration.py          — graph traversal: greedy stamina walk, path enumeration
├── location_manager.py     — BST + hash table: range queries, top-k, dynamic updates
├── reward_seeker.py        — max-heap-backed repeated highest-reward extraction
├── reward_structure.py     — RewardEntry, RewardStatus, RewardMaxHeap (heap + position index)
├── leaderboard.py          — merge sort + stable two-leaderboard merge
├── algorithms/
│   ├── bubble_sort.py
│   ├── insertion_sort.py
│   ├── merge_sort.py
│   ├── quick_sort.py
│   └── selection_sort.py
├── data_structures/        — provided custom ADT implementations (ArrayList, BST,
│                              hash table, heap, linked structures, etc.) — no built-in
│                              list/dict/heapq used anywhere in this project
├── clayton.txt              — campus graph + leaderboard data, Clayton campus
├── malaysia.txt             — campus graph + leaderboard data, Malaysia campus
└── campus.py                — provided campus/location/connection/leaderboard loader
```

The `algorithms/` and `data_structures/` modules were supplied by the unit as the only permitted building blocks — no Python built-in `list`, `dict`, `set`, or `heapq` is used anywhere in the five files above; every container operation goes through one of these custom ADTs.

---

## Sample run

Each module includes inline test assertions that double as usage examples — run any file directly to see it load a campus and verify its own outputs:

```bash
python exploration.py
python leaderboard.py
python location_manager.py
python reward_seeker.py
```

Example, `location_manager.py` querying Clayton campus for locations with a desirability score between 1.5 and 6.0:

```python
location_manager = LocationManager('clayton')
locations_in_range = location_manager.get_locations_in_range(1.5, 6.0)
# → [(2.2, 'Robert Blackwood Hall'), ..., (6.0, 'Religious Centre')]
```

---

## Skills Demonstrated

Matching the right ADT to an access pattern rather than defaulting to a familiar one; formal best/worst-case time complexity analysis grounded in the actual structure used, not assumed; building on hand-rolled data structures without relying on language built-ins; and recognising the practical trade-offs (e.g. balanced vs. unbalanced trees) that complexity claims depend on.
