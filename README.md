# pyntercept
## tl;dr 
python library &amp; utility to intercepting and processing i/o of CLI/TUI 
programs using PTYs.

## explanation, possible questions, reasoning

**What are pseudo-terminals (PTY)?**<br>
It's a UNIX specific (Windows also supports it) form of interprocess 
communication. Think about it as channel which could provide bidirectional flow 
of data between two programs. It also provides child process with some terminal
services (size, list of supported colors, etc).

**Why is that even needed?**<br>
It's needed for situations when you need to run terminal application without 
terminal.

**Why on earth even run terminal applications without a terminal!?**<br>
For example: when you connected to the server via SSH - the server isn't 
running a terminal, it just sends data through the internet to the client.
But some programs on the server expects to be executed in the terminal, to know 
how exactly to render data (e.g. `vim`, `nano`), so SSH server provides 
pseudo-terminal for them.

**It seems like a very niche use case for that, are any other usages for PTYs?**<br>
Interesting fact: I didn't use above the term `terminal emulator` and thats not 
for brevity.
PTYs are used when you don't have a real physical terminal device like VT-100.
When you are opening `terminal emulator` such as `Konsole`, under the hood there
is runned pseudo-terminal.

**So the use cases are following:**<br>
- terminal emulators (`xterm`, `konsole`, `yakuake`)
- ssh servers.
- terminal multiplexers (`GNU screen`, `tmux`, `zellij`).
- running terminal applications in environments without controlling terminal
  e.g. in child processes.
- i/o processing, e.g. keylogging like `GNU script` or automation tasks as 
`expect`, `pyexpect`.

The latter two use cases are the main focus for the `pyntercept`.  

# how does it work
```
┌─────────────┐       ┌───────────────┐
│ src (stdin) │       │ dest (stdout) │
└─────────────┘       └───────────────┘
 (1) │                         ^(6)      
     │   ┌─────────────────┐───┘        (0)┌────────────────┐
     └──>│ parent process  │──────────────>│ child process  │
         └─────────────────┘               └────────────────┘
          (2)│    ^(5)                     (4)│        ^(3)
        ┌─── v ── │ ───────────────────────── v ────── │ ────────┐
        │ ┌─────────────┐<─────────────────┌─────────────┐       │
        │ │ parent's fd │                  │ child fd    │       │
        │ └─────────────┘─────────────────>└─────────────┘       │
        │                                        ^               │
        │                  acts like a real terminal for the     │
        │                               child process            │
        │                                                        │
        └──────────────Pseudo terminal (PTY)─────────────────────┘                         
```

0.  parent process first allocates resources for processes interaction and then 
    runs child process with specified arguments and behaving as proxy object for 
    enteraction with child process.
1.  parent process receives input from source (by default stdin).
2.  then parent could do any transformations to it and 
    even could decide to send it to the child process or not.
3.  child process reads data from step (1) as its `stdin`.
4.  child process could generate some output and writes it into the child 
    terminal.
5.  parent process reads output sent by child process. Like in step 2, parent 
    process can transform output data and conditionally send it to the 
    destination as step (6).

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
-   optional dependencies `pyntercept[pyte]`, `pyntercept[rich]`, etc. 
-   filters, different rendering stages and strategies to give an ability to
    pass data into wider spectre of the programs.
-   wider support of external libraries, programs and use cases.
-   accumulate differences (like cursor movement or character changes) to 
    optimize rendering and support more environments and use cases.
-   support of Windows and other operating systems.
-   add built-in ability to specify areas of the terminal where to render data.
