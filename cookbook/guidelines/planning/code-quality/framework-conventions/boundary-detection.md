
1. **Framework-conventional units are the default scope group.** When the codebase follows framework conventions, those conventions define the scope groups. Do not decompose below the conventional unit without strong evidence from other lenses.
2. **Cross-feature sharing elevates to its own scope group.** A ViewModel or service referenced by three or more feature modules is no longer feature-local — it belongs in a shared scope group.
3. **Deviations are flagged, not respected.** If logic is placed in the wrong layer (business logic in a view), note the deviation — do not create a scope group that legitimizes the misplacement.
4. **Lazy-loaded modules are independent scope groups.** Any module configured for lazy loading in Angular, Next.js dynamic imports, or Webpack code splitting is designed to be independently loadable — treat it as an independent scope group.
5. **Plugin/extension registries are composition roots.** The registry that loads and wires plugins is a separate scope group from the plugins themselves.

