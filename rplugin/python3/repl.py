# file: repl.py
# auth: Libor Wagner <libor.wagner@cvut.cz>

import neovim


@neovim.plugin
class ReplSend(object):
    def __init__(self, nvim):
        self.nvim = nvim
        self.conf = self.nvim.vars['replsend_conf']

    @neovim.command('Repl', nargs='*', sync=True)
    def repl(self, args):
        # get current filetype and window
        ft = get_buffer_filetype(self.nvim.current.buffer)
        win = self.nvim.current.window

        # check whether we have repr configured
        if ft not in self.conf:
            self.nvim.err_write('No repl defined for {}'.format(ft))
            return

        # open new split with the terminal
        cmd = self.conf[ft]['bin'] + ' ' + ' '.join(self.conf[ft]['args'])
        self.nvim.command('vsplit | terminal ' + cmd)

        # get channel
        channel = int(self.nvim.command_output('echo &channel'))
        self.conf[ft]['channel'] = channel

        # go batch to the current window
        self.nvim.command('{}wincmd w'.format(win.number))

    @neovim.command('ReplSend', nargs='*', range='', sync=False)
    def repl_send(self, args, range):
        buf = self.nvim.current.buffer
        ft = get_buffer_filetype(buf)

        if ft not in self.conf or 'channel' not in self.conf[ft]:
            self.nvim.err_write('No repl for {} start repl first'.format(ft))
            return

        start, end = range

        # is it a visual selection
        visual = False
        if 'v' in args:
            visual = True

        if not visual and start == end:
            start, end = self.get_section(self.conf[ft], buf, start - 1)
        else:
            start = start - 1

        lines = buf[start:end]
        text = self.format(self.conf[ft], lines)
        self.nvim.call('chansend', self.conf[ft]['channel'], text)

    @neovim.command('ReplSendCmd', nargs='*', sync=False)
    def repl_send_cmd(self, nargs):
        buf = self.nvim.current.buffer
        ft = get_buffer_filetype(buf)

        if ft not in self.conf or 'channel' not in self.conf[ft]:
            self.nvim.err_write('No repl for {}, start repl first'.format(ft))
            return

        arg = ' '.join(nargs) + '\n'

        try:
            self.nvim.call('chansend', self.conf[ft]['channel'], arg)
        except neovim.api.NvimError as e:
            del self.conf[ft]['channel']
            self.nvim.err_write('No repl for {}, start repl first'.format(ft))

    def get_section(self, conf, buf, index):

        buflen = len(buf)
        
        # mark all commented regions
        iscomment = [False]*buflen
        if 'blockcomment' in conf:
            comment = False
            for i in range(buflen):
                if buf[i].startswith(conf['blockcomment']):
                    comment = not comment
                    iscomment[i] = True
                else:
                    iscomment[i] = comment
                    
        # get start
        i = index
        while i > 0:
            if buf[i].startswith(conf['section']) and not iscomment[i]:
                i = i + 1
                break
            i -= 1
        start = i

        # get end
        i = index + 1
        while i < buflen:
            if buf[i].startswith(conf['section']) and not iscomment[i]:
                break
            i += 1
        end = min(i, buflen)

        return (start, end)

    def format(self, conf, lines):

        # strip whitespaces
        if 'strip' in conf and conf['strip']:
            lines = [v.strip() for v in lines]

        # strip empty lines
        if 'noempty' in conf and conf['noempty']:
            lines = [v for v in lines if len(v) > 0]

        s = ''

        s += conf.get('prefix', '')
        s += conf.get('join', '\n').join(lines)
        s += conf.get('sufix', '')

        return s


def get_buffer_filetype(buf):
    return buf.options.get('filetype')


