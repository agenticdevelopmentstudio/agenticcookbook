
Objective-C gives no compile-time help with ownership or null unless you ask for it. ARC and nullability annotations turn the two largest sources of crashes into compiler diagnostics, and annotated headers are what let Swift callers use the code without force-unwraps. The rules cost little to follow when the header is first written and a great deal to retrofit.

