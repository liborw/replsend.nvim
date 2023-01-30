---
title:  REPL: My first Neovim plugin
author: Libor Wagner <libor.wagner@cvut.cz>
date:   2018-10-31
---

# ReplSend: Dead Simple Universel REPL

![replsend_sh](fig/replsend_sh.svg)

## Installation

Using [vim-plug](https://github.com/junegunn/vim-plug):

```
Plug 'liborw/replsend.nvim'

```

## Usage

 - `Repl` to start REPL based on current buffers filetype
 - `Repl <ft>` to start REPL with `<ft>` (usefull for markdown)
 - `ReplSend` sends section to REPL

## Configuration

Default configuration:

```lua
local default_options = {
  languages = {
    sh = {
      bin = "/usr/bin/bash",
      args = {},
      section_sep = "#%%",
      comment = "#",
      join = "\n",
      prefix = "\x1b[200~",
      suffix = "\x1b[201~\n",
    },
    python = {
      bin = "/usr/bin/python",
      args = {},
      section_sep = "#%%",
      comment = "#",
      join = "\n",
      prefix = "\x1b[200~",
      suffix = "\x1b[201~\n",
    },
    md = {
      bin = "/usr/bin/python",
      args = {},
      section_sep = "```",
      comment = "#",
      join = "\n",
      prefix = "\x1b[200~",
      suffix = "\x1b[201~\n",
    }
  }
}
```

Options:
 * **bin**: command to start for this filetype
 * **args**: arguments of that command
 * **section**: string used to split file into section, **ReplSend** will send just current section.
 * **prefix**: string placed before the input
 * **suffix**: string placed after the input
 * **join (default: \n)**: string used to join input lines
 * **strip (dafault: 0)**: strip whitespaces (not in lua version)
 * **noempy (defautl: 0)**: strip empty lines (not in lua version)
 * **comment (optional)**: comment characters (only single line comments are supported at the moment) (not in lua version)
 * **nocomments (defautl: 0):** remove comment from input (not in lua version)


## Limitations

 - Only single REPL for session

## Roadmap

 - [x] start terminal with apropriate repl based on filetype
 - [x] send selectin or section into terminal.
 - [x] basic configuration (binary, prefix, sufix, section markers)
 - [x] get back to the current buffer when opening REPL.
 - [x] for markdown start REPL with different filetypes
 - [x] lua implementation
 - [ ] make it more user friendly

## References

 - [repl.nvim](https://gitlab.com/HiPhish/repl.nvim)
 - [nvim-repl](https://github.com/justinmk/nvim-repl)
 - [How to debug neovim plugins](https://blog.rplasil.name/2016/03/how-to-debug-neovim-python-remote-plugin.html)

