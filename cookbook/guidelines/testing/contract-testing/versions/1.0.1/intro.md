
# Contract testing for services

A contract test verifies that two independently deployed services agree on the shape of the messages they exchange — without standing up the whole system. It catches the integration breakage that unit tests miss and end-to-end tests catch too late and too expensively.

When an AI codegen system emits several interoperating services (microservices, a web backend, mobile/web clients), each side evolves on its own schedule. The blind spot is structural: each service's own tests pass, yet a renamed field or a changed status code silently breaks the boundary. Contract tests close that gap.

