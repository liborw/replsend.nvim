
local api = vim.api

local M = {}

local default_options = {
  languages = {
    sh = {
      bin = "",
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
    mdpy = {
      bin = "/usr/bin/python",
      args = {},
      section_sep = "```",
      comment = "#",
      join = "\n",
      prefix = "\x1b[200~",
      suffix = "\x1b[201~\n",
    },
    mdsh = {
      bin = "",
      args = {},
      section_sep = "```",
      comment = "#",
      join = "\n",
      prefix = "\x1b[200~",
      suffix = "\x1b[201~\n",
    }
  }
}


M.options = default_options
M.filetype = nil
M.channel = nil

function M.setup(options)

  if options then
    M.options = options
  else
    M.options = default_options
  end

  vim.api.nvim_create_user_command("Repl", function (args) M.start(args.args) end, {nargs='?'})
  vim.api.nvim_create_user_command("ReplSend", M.send, {range="%"})

end

local function get_filetype(forced)
  local ft
  if forced ~= nil and forced ~= "" then
    ft = forced
  else
    ft = vim.bo.filetype
  end
  return ft
end

function M.start(lang)
  local win = api.nvim_get_current_win()

  local ft = get_filetype(lang)
  local opt = M.options.languages[ft]
  if opt == nil then
    vim.api.nvim_err_writeln('No REPL defined for ' .. ft)
    return
  end

  api.nvim_command("vsplit | term " .. opt.bin)
  M.filetype = ft
  vim.cmd('startinsert')
  vim.cmd('stopinsert')
  M.channel = tonumber(api.nvim_command_output("echo &channel"))
  vim.api.nvim_set_current_win(win)
end

local function get_section(lines, row, sep)

  local i0 = row
  while i0 > 1
  do
    if lines[i0]:find(sep,  1, true) then
      i0 = i0 + 1
      break
    end
    i0 = i0 - 1
  end

  local i1 = row + 1
  while i1 < #lines
  do
    if lines[i1]:find(sep,  1, true) then
      i1 = i1 - 1
      break
    end
    i1 = i1 + 1
  end

  if i1 > #lines then
    i1 = #lines
  end

  return i0, i1
end

function M.send(args)
  local buf = api.nvim_get_current_buf()
  local lines = api.nvim_buf_get_lines(buf, 0, -1, false)
  local win = api.nvim_get_current_win()

  -- Check whether we have already openned repl
  if M.channel == nil then
    vim.api.nvim_err_writeln('REPL not started')
    return
  end

  local opt = M.options.languages[M.filetype]

  local from, to
  if args.range ~= 0 then
    from = args.line1
    to = args.line2
  else
    local row = vim.api.nvim_win_get_cursor(win)[1]
    from, to = get_section(lines, row, opt.section_sep)
  end

  local code = {}
  table.insert(code, opt.prefix)
  for i = from,to do
    if lines[i]:find(opt.comment, 1, true) ~= 1 then
      table.insert(code, lines[i])
    end
  end
  table.insert(code, opt.suffix)

  local input = table.concat(code, opt.join)
  vim.api.nvim_chan_send(M.channel, input)
end


return M
