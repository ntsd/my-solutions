code = """input()
print(max((-int(i)**2,i)for i in raw_input().split()or"0")[1])""".encode().decode('utf16')

print(code)

exec(bytes(code,'u16')[2:])
