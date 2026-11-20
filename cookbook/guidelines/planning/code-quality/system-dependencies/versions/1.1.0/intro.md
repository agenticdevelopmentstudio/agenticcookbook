
# System Dependencies

Code that reaches into an OS framework, hardware API, or external service is fundamentally different from code that operates only on its own data. System dependencies reveal the technical surface area of a scope group — what the host platform must provide, what permissions are implied, and what cannot be easily mocked or isolated. This lens catalogs every external system the code touches to characterize the integration profile of each candidate scope group.

