
- Classes you own **SHOULD** declare dependencies via an `@Inject constructor`. Hilt then provides them without a module.
- Use a `@Module` with `@Provides` only for types you do not own (third-party, builders) or interfaces. Bind an interface to its implementation with `@Binds` in an `abstract` module — it generates less code than `@Provides`.
- Install every module into a component with `@InstallIn(...)`. Choose the **narrowest** component that fits the binding's lifetime.

