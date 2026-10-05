
An XcodeGen-generated Xcode project with app targets for all five Apple platforms, each displaying a component catalog: a navigable list of every UI component implemented from `ui/` specs, showing all states for visual testing and snapshot verification. The XcodeGen Apple Project ingredient provides the targets, shared package, and source layout; the Component Catalog ingredient provides what each app shows. The recipe wires them together through a shared source directory and per-platform entry points.

