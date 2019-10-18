print((lambda s:s%s)('print((lambda s:s%%s)(%r))'))

s='s=%r;print(s%%s)';print(s%s)
