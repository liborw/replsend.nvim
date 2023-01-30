
local api = vim.api
local uv = vim.loop

local M = {}

local default_options = {
  section_sep = "#%%",
  comment = "#"

}

M.options = default_options

function M.setup(options)

  if options then
    M.options = options
  else
    M.options = default_options
  end

end



function M.start()
  local buf = api.nvim_get_current_buf()
  local filetype = 'python'


end


local function get_section(lines, row, sep)

  local i0 = row
  while i0 >= 0
  do
    if lines[i0]:find(sep,  1, true) then
      break
    end
    i0 = i0 - 1
  end

  local i1 = row + 1
  while i1 < #lines
  do
    if lines[i1]:find(sep,  1, true) then
      break
    end
    i1 = i1 + 1
  end


  return i0, i1
end

function M.send()
  local buf = api.nvim_get_current_buf()
  local lines = api.nvim_buf_get_lines(buf, 0, -1, false)

  -- in what mode we are
  local mode = api.nvim_get_mode()["mode"]
  local from, to
  if mode == 'v' then
    from = vim.api.nvim_buf_get_mark(0, "<")[1]
    to = vim.api.nvim_buf_get_mark(0, ">")[1]
  else
    local row = vim.api.nvim_win_get_cursor(buf)[1]
    from, to = get_section(lines, row, M.options.section_sep)
  end

  vim.api.nvim_echo({{string.format("start: %s end: %s", from, to)}}, false, {})

  local code = {}
  for i = from,to do
    if lines[i]:find(M.options.comment, 1, true) ~= 1 then
      table.insert(code, lines[i])
    end
  end



end

function M.status()

  local start_win = vim.api.nvim_get_current_win()

  vim.api.nvim_command('botright vnew')
  local win = vim.api.nvim_get_current_win()
  local buf = vim.api.nvim_get_current_buf()

  vim.api.nvim_buf_set_name(buf, 'Equals Status #' .. buf)
  vim.api.nvim_buf_set_option(buf, 'buftype', 'nofile')
  vim.api.nvim_buf_set_option(buf, 'swapfile', false)
  vim.api.nvim_buf_set_option(buf, 'bufhidden', 'wipe')


  local list = {}

  table.insert(list, "# Options")

  table.insert(list, string.format(" filetype: %s", vim.bo.filetype))

  vim.api.nvim_buf_set_lines(buf, 0, -1, false, list)
end


return M
