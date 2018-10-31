---
title:  REPL: My first Neovim plugin
author: Libor Wagner <libor.wagner@cvut.cz>
date:   2018-10-31
---

# REPL: My first Neovim plugin



## Testing neovim client in interactive session

 - First start the neovim with `NVIM_LISTEN_ADDRESS` set.

```
NVIM_LISTEN_ADDRESS=/tmp/nvim nvim
```

 - Then in python/ipython

```python
import neovim

nvim = neovim.attach('socket', path='/tmp/nvim')
nvim.command('echo "test"')
```

 - And `test` should appear in the command section

## Notes

 - Get filetype of buffer: `buf.options.get('filetype')`
 - Get channel of terminal: `nvim.command_output(echo &channel)`
 - Send enter to channel


## References

 - [repl.nvim](https://gitlab.com/HiPhish/repl.nvim)
 - [nvim-repl](https://github.com/justinmk/nvim-repl)


