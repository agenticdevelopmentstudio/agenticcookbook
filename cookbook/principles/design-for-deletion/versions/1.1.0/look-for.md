
- `should-build-disposable-software`: code shaped for reuse no current caller needs, at the cost of being easy to discard
- `should-write-code-easy-to-throw-away`: code whose removal would ripple into the rest of the system
- `should-treat-lines-as-spent`: code kept that could be deleted
- `should-not-abstract-prematurely-for-reuse`: an abstraction introduced for reuse before a second use exists
- `should-duplicate-rather-than-couple-when-in-doubt`: two uncertain-fit pieces of code coupled through a shared dependency where duplication would do
