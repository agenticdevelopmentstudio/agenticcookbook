
- Since Ruby 3.0 positional hashes and keyword arguments are separate. Code MUST pass a hash as keywords with `**opts` explicitly, and accept it with `**opts`.
- A method that forwards its arguments MUST declare `*args, **kwargs, &block` or use `...`. `ruby2_keywords` SHOULD be used only in code that must also run on Ruby 2.6 to 3.0.

