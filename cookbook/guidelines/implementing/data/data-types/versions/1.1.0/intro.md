
# Data types and type affinity

SQLite uses dynamic typing: the value determines the type, not the column declaration. A column's declared type is a preference called "affinity," not a hard constraint (unless STRICT mode is used). Understanding this is essential to writing correct schemas.

