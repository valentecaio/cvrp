# cast ' abc 123 ' to 'abc 123'
def remove_spaces_in_borders(str):
  while(len(str) > 0 and str[0] == ' '):
    str = str[1:]
  while(len(str) > 0 and str[-1] == ' '):
    str = str[:-1]
  return str

# returns a list of lines
def extract_section(s, flag_start, flag_end):
  return s[s.find(flag_start)+len(flag_start):s.find(flag_end)].split('\n')[1:-1]
