
# Adopt Swift 6 strict concurrency incrementally

The Swift 6 language mode turns data-race safety into a **compile-time** guarantee: the compiler statically rejects code that could race. Adopt it module by module so each isolation boundary is fixed in isolation rather than fighting the whole graph at once.

