
- For every changed function, read its comment and docstring against the new body. Check parameters, return values, errors raised, side effects and units.
- Flag a comment that explains a branch, a workaround or a constant the change removed or altered.
- Flag comments that narrate history ("now we", "previously", "changed to") instead of stating what is true now. History belongs in version control.
- Check the neighbors too. A docstring above an untouched function can be made false by a change in what it calls.

