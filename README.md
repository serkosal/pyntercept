# pyntercept
python library &amp; utility to intercept i/o from interactive CLI/TUI programs.

# installation

## to install pyntercept as program

using pipx
```console
pipx install pyntercept
```

## to install pyntercept as library

```console
pip install pyntercept
```

# roadmap
-   curses support of 256, true colors.
-   fix rendering with `rich` python library.
-   abstract class to generilize rendering with different backends.
-   optional dependencies `pyntercept[pyte]`, `pyntercept[rich]`, etc. 
-   filters, different rendering stages and strategies to give an ability to
    pass data into wider spectre of the programs.
-   wider support of external libraries, programs and use cases.
-   accumulate differences (like cursor movement or character changes) to 
    optimize rendering and support more environments and use cases.
-   support of Windows and other operating systems.
-   add built-in ability to specify areas of the terminal where to render data.
