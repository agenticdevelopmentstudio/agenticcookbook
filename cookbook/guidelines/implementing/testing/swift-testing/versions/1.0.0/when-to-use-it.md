
- For new Swift **unit tests**, you **SHOULD** author with Swift Testing rather than XCTest.
- You **MUST NOT** rewrite passing XCTest suites solely to switch frameworks; migrate opportunistically when a test changes.
- XCTest is **still required** for UI tests (`XCUIApplication`) and for XCTest-based performance measurement (`measure {}`); Swift Testing does not replace these as of Xcode 16. Keep those in XCTest.

