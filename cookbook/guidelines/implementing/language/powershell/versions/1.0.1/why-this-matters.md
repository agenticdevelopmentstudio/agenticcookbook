
PowerShell's defaults favor an interactive session: errors keep going, typos in variable names are `$null`, and any expression leaks into output. Strict mode, a Stop preference and disciplined output turn the same script into one that fails where the mistake is, and `-WhatIf` lets a person see a destructive change before it happens.

