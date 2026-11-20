
# Cross-Cutting Detection

Some code appears everywhere. Logging calls exist in every file. Error handling patterns repeat across every service. Analytics events fire from every user action. These are cross-cutting concerns — they cut across the grain of the architecture rather than residing in a single layer. The critical distinction is between concerns that are truly cross-cutting (woven into every group and impossible to isolate) and concerns that look cross-cutting but are actually shared infrastructure with clear ownership. Getting this wrong in either direction distorts the scope group map.

