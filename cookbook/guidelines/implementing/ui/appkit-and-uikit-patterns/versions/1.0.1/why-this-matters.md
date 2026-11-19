
AppKit and UIKit already solve routing, ownership of callbacks, threading and lifecycle. Code that uses those mechanisms is short and behaves like the rest of the platform; code that works around them (global references for actions, strong delegates, UI work on background queues) is where retain cycles, crashes and missed teardown come from.

