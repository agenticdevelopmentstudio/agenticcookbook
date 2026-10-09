
# Never overwrite a user's files

Skills, commands, agents and rules are installed into directories the user also writes to. Those directories are shared resources: the user may already have a file with the same name, and an install that replaces it destroys work the user cannot get back. This applies whichever tool reads the directory.

