
Raising deploy frequency *without* also improving architecture and test coverage typically makes things worse before better — DORA calls this the J-curve. Automation surfaces latent technical debt and manual test burden, so failure rates and toil rise during the dip before performance recovers.

- Teams **MUST NOT** treat "deploy more often" as a goal independent of test and architecture investment.
- Teams **SHOULD** adopt continuous *deployment* only once automated tests and a decoupled architecture genuinely support it; until then, continuous *delivery* with a human release gate is the safer default.
- Expect a temporary performance dip when adopting CD; plan for the recovery rather than abandoning the effort at the bottom of the curve. (Caveat: the J-curve is an observed pattern, not a guarantee; depth and duration vary by team.)

