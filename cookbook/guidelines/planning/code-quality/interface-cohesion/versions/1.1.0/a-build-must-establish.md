
- `should-group-protocol-with-primary-implementation`: every protocol and its primary implementation share a recommended group, or the implementation is 50+ files, or the findings say why not
- `should-treat-barrel-reexports-as-one-candidate`: every barrel's re-exported subdirectories form one candidate, or separate groups sharing a common API layer, or the findings say why not
- `should-place-shared-types-with-primary-consumer`: every shared type sits in its primary consumer's group, or the findings say why not
- `should-note-fragmented-interfaces`: every interface declared across three or more files with no barrel is listed under cohesion anomalies
- `should-not-count-internal-helpers-as-interface`: no private, internal or file-private symbol appears in an interface surface's lists
- `should-attend-to-protocol-extension-pairs`: every Swift protocol's extensions in other files are listed with it
- `should-treat-java-interface-triads-as-one-unit`: every Java interface + abstract class + primary implementation triad is in one group, or the findings say why not
