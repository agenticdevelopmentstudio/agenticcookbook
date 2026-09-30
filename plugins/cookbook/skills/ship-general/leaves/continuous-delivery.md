<!-- leaf: ship-general/continuous-delivery · source: guidelines/shipping/continuous-delivery.md -->

**Rules** (cite as `ship-general/continuous-delivery#<slug>`):

- `pipeline-keep-main-releasable-whether` MUST — The pipeline MUST keep main releasable. Whether releases auto-ship is a separate choice.
- `change-not-merge-main-leaves-main` MUST — A change MUST NOT merge to main if it leaves main un-releasable.
- `pipeline-fully-automated-from-commit` MUST — The pipeline MUST be fully automated from commit to a deployable artifact: build, test, package, and (for deployment) …
- `commit-main-trigger-pipeline-red-pipeline` MUST — Every commit to main MUST trigger the pipeline; a red pipeline MUST block release and SHOULD be treated as a …
- `pipeline-produce-single-immutable-artifact` MUST — The pipeline MUST produce a single immutable artifact promoted unchanged across environments (build once, deploy many). …
- `deployments-reversible-prefer-fast-rollback` SHOULD — Deployments SHOULD be reversible: prefer a fast rollback or roll-forward path, and decouple deploy from release using …
- `pipeline-feedback-fast-minutes-hours-slow` SHOULD — Pipeline feedback SHOULD be fast (minutes, not hours); slow pipelines erode the tight-feedback-loops the practice …
- `teams-not-treat-deploy-more-often` MUST — Teams MUST NOT treat "deploy more often" as a goal independent of test and architecture investment.
- `teams-adopt-continuous-deployment-only` SHOULD — Teams SHOULD adopt continuous *deployment* only once automated tests and a decoupled architecture genuinely support it; …

# Continuous delivery

Continuous delivery (CD) keeps the main branch in an always-releasable state through an automated build-test-deploy pipeline, so that shipping is a button press rather than a manual scramble. It is the infrastructure that makes the rigor-versus-velocity trade-off non-zero-sum, operationalizing small-reversible-decisions and tight-feedback-loops.

## Delivery vs. deployment

These are distinct practices; do not conflate them.

| Practice | What it means | Who decides to release |
|----------|---------------|------------------------|
| Continuous **delivery** | Every change that passes the pipeline is *deployable* to production at any time. | A human / business decision (a button press). |
| Continuous **deployment** | Every change that passes the pipeline is *automatically deployed* to production. | The pipeline, with no manual gate. |

- The pipeline MUST keep main releasable. Whether releases auto-ship is a separate choice.
- A change MUST NOT merge to main if it leaves main un-releasable.

## Pipeline requirements

- The pipeline **MUST** be fully automated from commit to a deployable artifact: build, test, package, and (for deployment) deploy — no manual steps in the path to "releasable."
- Every commit to main **MUST** trigger the pipeline; a red pipeline **MUST** block release and **SHOULD** be treated as a stop-the-line event.
- The pipeline **MUST** produce a single immutable artifact promoted unchanged across environments (build once, deploy many). Do not rebuild per environment.
- Deployments **SHOULD** be reversible: prefer a fast rollback or roll-forward path, and decouple deploy from release using flags (see related: feature-flags) so risky changes ship dark.
- Pipeline feedback **SHOULD** be fast (minutes, not hours); slow pipelines erode the tight-feedback-loops the practice exists to provide.

## The J-curve caveat

Raising deploy frequency *without* also improving architecture and test coverage typically makes things worse before better — DORA calls this the J-curve. Automation surfaces latent technical debt and manual test burden, so failure rates and toil rise during the dip before performance recovers.

- Teams **MUST NOT** treat "deploy more often" as a goal independent of test and architecture investment.
- Teams **SHOULD** adopt continuous *deployment* only once automated tests and a decoupled architecture genuinely support it; until then, continuous *delivery* with a human release gate is the safer default.
- Expect a temporary performance dip when adopting CD; plan for the recovery rather than abandoning the effort at the bottom of the curve. (Caveat: the J-curve is an observed pattern, not a guarantee; depth and duration vary by team.)

## Pre-PR checklist for agents

1. Confirm CI runs the full automated pipeline on this branch and is green before marking the PR ready.
2. Confirm the change does not require a manual step to become releasable.
3. Confirm risky behavior is gated behind a flag so merge does not force a release.
4. Confirm a rollback or roll-forward path exists for the change.
