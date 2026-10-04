
- Pair this with **infrastructure-as-code** (see related): the artifact is built from version-controlled definitions (`Dockerfile`, Packer template) so builds are reproducible and reviewable.
- Containers are the common implementation, but the principle predates and outlives them — a baked VM image (Packer/AMI) is equally immutable.
- Provisioning of replacement instances **SHOULD** be automated end-to-end so replacement is routine, not a manual event.

