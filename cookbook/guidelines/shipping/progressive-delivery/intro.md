
# Progressive delivery

Progressive delivery separates *deploy* (code reaches production servers) from *release* (users see behavior), then exposes the change to a growing audience while watching health signals. It builds on continuous-delivery (the pipeline that produces a deployable build) and feature-flags (the control plane that gates exposure). The goal is to limit blast radius and roll back fast when signals degrade.

