
A three-mode toggle button that cycles between automatic, forced dark, and forced light appearance modes. Automatic mode (the default) follows the operating system's appearance setting in real time. The two forced modes override the system preference.

This recipe is intentionally agnostic about how site settings are stored. The consuming site provides its own persistence mechanism ("site settings") — localStorage, cookies, a database, or any other store. The recipe specifies what to read, write, and clear, but not where.

