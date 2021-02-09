#TartanLama/Expected pretty printer for gdb

Pretty prints [tl::expected](https://github.com/TartanLlama/expected) in GDB. Also provides better output for GDB based debuggers like CLion.

## Installing the pretty printer

This will install the pretty printer globally, so every instance of gdb can use the improved output. 

- clone this repository
- reate a .gdbinit in the $HOME of your user if it doesn't exist alread
- add the following entry to your.gdbinit :
    ```
    python
    import sys
    import gdb
    sys.path.insert(0, "<PATH>")
    from TlExpectedPrinter import register_printer
    gdb.pretty_printers.append(register_printer)
    end
    ```
- change \<PATH\> to the path of this repository (using \\\ as a path separator under windows)
- gdb should now use the pretty printer to format any tl::expected<X, Y>