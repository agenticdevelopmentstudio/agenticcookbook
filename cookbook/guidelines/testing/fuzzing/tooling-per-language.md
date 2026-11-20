
| Language | Engine / tool | Notes |
|----------|---------------|-------|
| C / C++ | libFuzzer, AFL++, Honggfuzz | Run with sanitizers (ASan/UBSan/MSan). |
| Rust | `cargo-fuzz` (libFuzzer) | Use `arbitrary` for structured inputs. |
| Go | native `go test -fuzz` (since Go 1.18) | `testing.F` corpus + mutator. |
| JVM | Jazzer (libFuzzer-backed, in-process) | Java/Kotlin/Scala. |
| Python | Atheris (libFuzzer-backed) | Native-extension and pure-Python targets. |

FORECAST (recent, unverified-for-production): a 2026 Go-toolchain fork (`gosentry`/LibAFL-backed `go test -fuzz`) advertises struct-aware and grammar-based fuzzing.
