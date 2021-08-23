import string


charlist = list(string.printable)

fib = [1, 1]
for i in range(2, 11):
	fib.append(fib[i - 1] + fib[i - 2])

def c2f(c):
	n = ord(c)
	b = ''
	for i in range(10, -1, -1):
		if n >= fib[i]:
			n -= fib[i]
			b += '1'
		else:
			b += '0'
	return b


enc_charlist = [c2f(i) for i in charlist]
charlist = dict(zip(charlist, enc_charlist))

with open("flag.enc") as enc:
	flag = enc.read()
	for k, v in charlist.items():
		flag = flag.replace(v, k)
	print(flag)
	
