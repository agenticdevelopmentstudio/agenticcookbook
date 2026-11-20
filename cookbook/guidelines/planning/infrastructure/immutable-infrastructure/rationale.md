
- `should-treat-running-instances-as-read-only`, `must-rebuild-to-change`: This eliminates **configuration drift**: every instance of version `vN` is byte-identical, so "works on that box but not this one" cannot happen.
- `must-ship-immutable-versioned-artifacts`: Containers are the common implementation, but the principle predates and outlives them — a baked VM image (Packer/AMI) is equally immutable.
- `should-adopt-heavier-machinery-only-on-measured-need`: This applies wherever you deploy servers; you do not need an orchestrator to benefit. A single image redeployed to one VM already gives you reproducibility and clean rollback.
