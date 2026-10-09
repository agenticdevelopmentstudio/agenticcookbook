
- Use one line-ending convention across Windows, WSL and containers. Set it in `.gitattributes` per file type, not in each developer's global configuration, and keep shell scripts as LF: a script with CRLF endings fails in Linux with confusing errors.
- Install Git in each file system you use it from, and make sure each is configured for the same convention.

