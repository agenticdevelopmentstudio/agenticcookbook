
- `should-classify-topic-type-before-searching`: searching begun with no type (medical, technical, legal, financial, news, consumer, …) set for the topic
- `should-select-authoritative-sources-by-type`: sources counted as authoritative because of the user's wording or urgency rather than the topic's type
- `should-set-evidence-bar-by-type`: one evidence bar applied to claims of different types, such as a treatment claim held only to a recipe claim's standard
- `should-not-carry-method-across-types`: a method that fits one type used for another, such as web consensus for a treatment claim
- `should-classify-each-claim-by-its-type`: a topic spanning types whose claims all take the topic's one type instead of the type each asserts
