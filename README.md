---
title:  REPL: My first Neovim plugin
author: Libor Wagner <libor.wagner@cvut.cz>
date:   2018-10-31
---

# REPL: My first Neovim plugin

After strugling with [iron.vim](https://github.com/Vigemus/iron.nvim), [vim-slime](https://github.com/jpalardy/vim-slime) and other similar plugins I have decided to write my own. One that would be simple, did what I want, and worked with python and matlab. It is written as a remote python plugin using the [python-client](https://github.com/neovim/python-client) module. And it is a first neovim and vim plugin ever.


## Installation
## Testing neovim client in interactive session

Using [vim-plug](https://github.com/junegunn/vim-plug):

```
Plug 'liborw/replsend.nvim', {'do': ':UpdeteRemotePlugins'}

```

## Configuration

The proper configuration does not yet work, but the idea is similar to that of [].

```
let g:replsend_conf = {"python":{"bin":"ipython", "section":"##",...}}
```

## Usage

There are just two commands:

* **Repl** will start REPL based on the configuration.
* **ReplSend** will send selection or section to the REPL.

## Limitations

 - Only single REPL for each filetype

## Roadmap

 - [x] start terminal with apropriate repl based on 
 - [x] send selectin or section into terminal.
 - [ ] basic configuration (binary, prefix, sufix, section markers)
 - [ ] get back to the current buffer when opening REPL.

## References

 - [repl.nvim](https://gitlab.com/HiPhish/repl.nvim)
 - [nvim-repl](https://github.com/justinmk/nvim-repl)
 - [How to debug neovim plugins](https://blog.rplasil.name/2016/03/how-to-debug-neovim-python-remote-plugin.html)

