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

I tis is example of my config:

```
let g:replsend_conf = {}
let g:replsend_conf['matlab'] = {
            \"bin":"matlab",
            \"args":["-nodesktop", "-nosplash"],
            \"section":"%%",
            \"prefix":"",
            \"sufix":"\n",
            \"join":",",
            \"strip":1,
            \"noempty":1,
            \"comment":"%",
            \"nocomments":1
            \}
let g:replsend_conf['markdown'] = {
            \"bin":"ipython3",
            \"args":["--matplotlib"],
            \"section":"```",
            \"prefix":"\x1b[200~",
            \"sufix":"\x1b[201~\n\n",
            \"join":"\n",
            \}
let g:replsend_conf['python'] = {
            \"bin":"ipython3",
            \"args":["--matplotlib"],
            \"section":"#%%",
            \"prefix":"\x1b[200~",
            \"sufix":"\x1b[201~\n\n",
            \"join":"\n",
            \}
let g:replsend_conf['sh'] = {
            \"bin":"",
            \"args":[],
            \"section":"#%%",
            \"prefix":"\x1b[200~",
            \"sufix":"\x1b[201~\n",
            \"join":"\n",
            \"noempty":1
            \}
```

Options:
 * **bin**: command to start for this filetype
 * **args**: arguments of tat command
 * **section**: string used to split file into section, **ReplSend** will send just current section.
 * **prefix**: string used befor the input 
 * **suffix**:
 * **join**:
 * **strip (optional)**:
 * **noempy (optional))** :
 * **comment (optional)**:
 * **nocomments (optional):
 

## Usage

There are just two commands:

* **Repl** will start REPL based on the configuration.
* **ReplSend** will send selection or section to the REPL.
* **ReplSendCmd** send argument of this command to the REPL 

## Limitations

 - Only single REPL for each filetype

## Roadmap

 - [x] start terminal with apropriate repl based on filetype
 - [x] send selectin or section into terminal.
 - [x] basic configuration (binary, prefix, sufix, section markers)
 - [x] get back to the current buffer when opening REPL.

## References

 - [repl.nvim](https://gitlab.com/HiPhish/repl.nvim)
 - [nvim-repl](https://github.com/justinmk/nvim-repl)
 - [How to debug neovim plugins](https://blog.rplasil.name/2016/03/how-to-debug-neovim-python-remote-plugin.html)

