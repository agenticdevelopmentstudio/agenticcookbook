
Ruby's defaults are permissive: strings are mutable, a command string goes to the shell, `rescue` swallows broadly. Opting into the strict form in each file keeps scripts predictable and keeps untrusted input away from a shell.

