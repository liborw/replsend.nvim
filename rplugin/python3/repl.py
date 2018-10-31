
import neovim


@neovim.plugin
class Repl(object):
    def __init__(self, nvim):
        self.nvim = nvim
        self.calls = 0
        # self.conf = self.nvim.vars['repl_conf']

        self.conf = {
            "python": {
                "bin": "ipython",
                "section": "##",
                "prefix": "\x1b[200~",
                "sufix": "\x1b[201~\n\n"
                },
            "markdown": {
                "bin": "ipython",
                "section": "```",
                "prefix": "\x1b[200~",
                "sufix": "\x1b[201~\n\n"
                }
        }

    @neovim.command('Repl', nargs='*', sync=True)
    def repl(self, args):
        ft = get_buffer_filetype(self.nvim.current.buffer)

        if ft not in self.conf:
            self.nvim.err_write('No repl defined for {}'.format(ft))
            return

        self.nvim.command('vsplit | terminal ' + self.conf[ft]['bin'])
        self.conf[ft]['channel'] = int(self.nvim.command_output('echo &channel'))

    @neovim.command('ReplSend', nargs='*', range='', sync=True)
    def repl_send(self, args, range):
        buf = self.nvim.current.buffer
        ft = get_buffer_filetype(buf)

        if ft not in self.conf or 'channel' not in self.conf[ft]:
            self.nvim.err_write('No repl for {} start repl first'.format(ft))
            return

        start, end = range

        if start == end:
            start, end = self.get_section(self.conf[ft], buf, start)
        else:
            start = start - 1
            end = end
        
        self.nvim.command('echo "range {}:{}"'.format(start, end))

        lines = buf[start:end]
        text = self.format(self.conf[ft], lines)
        self.nvim.call('chansend', self.conf[ft]['channel'], text)

    def get_section(self, conf, buf, index):

        buflen = len(buf)

        # get start
        i = index
        while i > 0:
            if buf[i].startswith(conf['section']):
                i = i + 1
                break
            i -= 1
        start = i

        # get end
        i = index + 1
        while i < buflen:
            if buf[i].startswith(conf['section']):
                i = i - 1
                break
            i += 1
        end = min(i, buflen-1)

        return (start, end)

    def format(self, conf, lines):

        s = ''

        s += conf.get('prefix', '')
        s += '\n'.join(lines)
        s += conf.get('sufix', '')

        return s


def get_buffer_filetype(buf):
    return buf.options.get('filetype')


