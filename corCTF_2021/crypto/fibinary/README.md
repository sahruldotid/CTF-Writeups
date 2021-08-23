# Fibinary

> Warmup your crypto skills with the superior number system!

Given 2 files, enc.py and flag.enc. From the name we know that the flag is encrypted using python script. So, lets look into enc.py and flag.enc



**flag.enc**

```
10000100100 10010000010 10010001010 10000100100 10010010010 10001000000 10100000000 10000100010 00101010000 10010010000 00101001010 10000101000 10000010010 00101010000 10010000000 10000101000 10000010010 10001000000 00101000100 10000100010 10010000100 00010101010 00101000100 00101000100 00101001010 10000101000 10100000100 00000100100
```

**enc.py**

~~~python
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

flag = open('flag.txt', 'r').read()
enc = ''
for c in flag:
	enc += c2f(c) + ' '
with open('flag.enc', 'w') as f:
	f.write(enc.strip())
~~~



The interesting code is

~~~python
flag = open('flag.txt', 'r').read()
enc = ''
for c in flag:
	enc += c2f(c) + ' '
~~~



By looking at the piece above, we know that our flag is encrypted using c2f() per character. Therefore, we dont need to understanding what the c2f() function does. We just need brute force the flag by generating all ascii character and pass it into c2f() function. And then we can replace encrypted flag with our ascii value. 

**solver.py**

~~~python
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
~~~



**FLAG:** corctf{b4s3d_4nd_f1bp!113d}

