
# Twelve-factor configuration

Strictly separate configuration from code. Everything that varies between deploys — credentials, service endpoints, and feature toggles — **MUST** be read from the environment, and the same build artifact **MUST** run unchanged in every environment.

