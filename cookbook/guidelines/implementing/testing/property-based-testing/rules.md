
- **should-use-property-tests-where-a-property-holds-for-all-inputs**: Property-based testing SHOULD be used for parsers, serializers, data transformers, encoders/decoders, validators — anything where "for all valid inputs X, property Y holds."
- **should-describe-properties-instead-of-examples**: Instead of testing specific examples, you SHOULD describe properties of the output and let the framework generate hundreds of random inputs to try to falsify them.
- **must-write-a-property-test-per-data-transformation**: At least one property test MUST be written per data transformation function; the examples below show such properties.

- **should-test-preservation-property-for-collection-operations**: A preservation property SHOULD be tested for collection operations.
