
- Casting between an Objective-C object pointer and a Core Foundation pointer MUST state who owns the result. Use `__bridge` when ownership does not change, `__bridge_retained` to hand an object to Core Foundation (you now `CFRelease` it), and `__bridge_transfer` to take a Core Foundation object into ARC (ARC now releases it).
- Never use a bare C cast between the two worlds in ARC code. The compiler rejects it for good reason.

