
- Since Ruby 3.0 positional hashes and keyword arguments are separate. Pass a hash as keywords with `**opts` explicitly, and accept it with `**opts`.
- A method that forwards its arguments declares `*args, **kwargs, &block` or uses `...`. Use `ruby2_keywords` only in code that must also run on Ruby 2.6 to 3.0.

