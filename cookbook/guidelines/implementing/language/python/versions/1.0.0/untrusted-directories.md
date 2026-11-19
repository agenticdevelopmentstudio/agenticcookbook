
- A script run from a directory you do not control can import a file planted next to it. Start it with `python -I` (isolated mode), which ignores the script directory, the user site-packages directory and every `PYTHON*` environment variable.
- Isolated mode implies `-E -P -s`. Be aware that `-m` puts the current directory on `sys.path`, so do not use `-m` from an untrusted working directory.
- Never run an interpreter inside a directory of downloaded files. Run it from your own directory and pass the downloaded path as an argument.

