
- The pipeline **MUST** be fully automated from commit to a deployable artifact: build, test, package, and (for deployment) deploy — no manual steps in the path to "releasable."
- Every commit to main **MUST** trigger the pipeline; a red pipeline **MUST** block release and **SHOULD** be treated as a stop-the-line event.
- The pipeline **MUST** produce a single immutable artifact promoted unchanged across environments (build once, deploy many). Do not rebuild per environment.
- Deployments **SHOULD** be reversible: prefer a fast rollback or roll-forward path, and decouple deploy from release using flags (see related: feature-flags) so risky changes ship dark.
- Pipeline feedback **SHOULD** be fast (minutes, not hours); slow pipelines erode the tight-feedback-loops the practice exists to provide.

