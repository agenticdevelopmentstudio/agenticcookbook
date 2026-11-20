
Batched, uncommitted changes create compound failures that are difficult to debug. When three changes interact in a broken build, isolating which change caused the failure requires significantly more effort than catching each failure as it occurs. Small, committed changes are also individually revertible, bisectable, and reviewable.

