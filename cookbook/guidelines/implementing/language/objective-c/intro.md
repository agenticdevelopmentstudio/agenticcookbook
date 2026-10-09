
# Objective-C

Objective-C code in a mixed or legacy Apple codebase MUST compile with ARC, MUST declare nullability in every public header, and MUST be shaped so Swift imports it as idiomatic Swift. Do not write new Objective-C where Swift will do; when the code must stay Objective-C (an existing module, a C++ interop shim, a framework with an Objective-C public surface), the rules below apply.

