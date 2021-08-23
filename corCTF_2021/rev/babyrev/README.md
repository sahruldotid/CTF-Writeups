# babyrev

> well uh... this is what you get when you make your web guy make a rev chall



given 1 ELF binary file, lets open it on IDA.

**main()**

~~~c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  char j; // al
  int i; // [rsp+8h] [rbp-F8h]
  int v6; // [rsp+Ch] [rbp-F4h]
  size_t v7; // [rsp+10h] [rbp-F0h]
  size_t n; // [rsp+18h] [rbp-E8h]
  char s[64]; // [rsp+20h] [rbp-E0h] BYREF
  char dest[64]; // [rsp+60h] [rbp-A0h] BYREF
  char s1[72]; // [rsp+A0h] [rbp-60h] BYREF
  unsigned __int64 v12; // [rsp+E8h] [rbp-18h]

  v12 = __readfsqword(0x28u);
  fgets(s, 64, stdin);
  s[strcspn(s, "\n")] = 0;
  v7 = strlen(s);
  n = 7LL;
  if ( strncmp("corctf{", s, 7uLL) )
    goto LABEL_12;
  if ( s[v7 - 1] != 125 )
    goto LABEL_12;
  if ( v7 != 28 )
    goto LABEL_12;
  memcpy(dest, &s[n], 28 - n - 1);
  dest[28 - n - 1] = 0;
  for ( i = 0; i < strlen(dest); ++i )
  {
    v6 = 4 * i;
    for ( j = is_prime(4 * i); j != 1; j = is_prime(v6) )
      ++v6;
    s1[i] = rot_n(dest[i], v6);
  }
  s1[strlen(s1) + 1] = 0;
  memfrob(check, 0x14uLL);
  if ( !strcmp(s1, check) )
  {
    puts("correct!");
    return 0;
  }
  else
  {
LABEL_12:
    puts("rev is hard i guess...");
    return 1;
  }
}
~~~

From the code above, we know that the flag length is **28**, start with **corctf{** and end with **}**. The program create loop and check the iterator is prime or not using **is_prime()** function and if some condition are true our input will be passed into **rot_n()** function. 



I very curious about the this code below, so i decided to debug it with gdb

~~~c
memfrob(check, 0x14uLL);
  if ( !strcmp(s1, check) )
  {
    puts("correct!");
    return 0;
  }
~~~

```
 ► 0x55555555558d <main+479>    call   strcmp@plt                <strcmp@plt>
        s1: 0x7fffffffdcf0 ◂— 0x444458524e4c4643 ('CFLNRXDD')
        s2: 0x555555558010 (check) ◂— 'ujp?_oHy_lxiu_zx_uve'
```

We got encoded flag here, ujp?_oHy_lxiu_zx_uve. Now lets explore another function in IDA

**rot_n()**

~~~c
__int64 __fastcall rot_n(unsigned __int8 a1, int a2)
{
  if ( strchr(ASCII_UPPER, (char)a1) )
    return (unsigned __int8)ASCII_UPPER[(a2 + (char)a1 - 65) % 26];
  if ( strchr(ASCII_LOWER, (char)a1) )
    return (unsigned __int8)ASCII_LOWER[(a2 + (char)a1 - 97) % 26];
  return a1;
}
~~~



**is_prime()**

~~~c
__int64 __fastcall is_prime(int a1)
{
  int i; // [rsp+1Ch] [rbp-4h]

  if ( a1 <= 1 )
    return 0LL;
  for ( i = 2; i <= (int)sqrt((double)a1); ++i )
  {
    if ( !(a1 % i) )
      return 0LL;
  }
  return 1LL;
}
~~~



At the first place, i dont know what the result of this loop at **main()**

~~~c
for ( j = is_prime(4 * i); j != 1; j = is_prime(v6) )
      ++v6;
~~~

so i decided to create c source code that implement the code all above.

**loop.c**

~~~C
#include <stdio.h>
#include <math.h>
#include <string.h>

// gcc loop.c -o loop -lm

int is_prime(int a1){
  int i;
  if ( a1 <= 1 )
    return 0;
  for ( i = 2; i <= sqrt(a1); ++i )
  {
    if ( !(a1 % i) )
      return 0;
  }
  return 1;
}



int main(int argc, char const *argv[])
{
	char flag[] = "ujp?_oHy_lxiu_zx_uve";
	int v6;
	for ( int i = 0; i < strlen(flag); ++i ){
	    v6 = 4 * i;
	    for ( int j = is_prime(4 * i); j != 1; j = is_prime(v6) )
	      ++v6;
	  	printf("%d ", v6);	    
	}
}
~~~

```
➜  babyrev git:(master) ✗ gcc loop.c -o loop -lm
➜  babyrev git:(master) ✗ ./loop
2 5 11 13 17 23 29 29 37 37 41 47 53 53 59 61 67 71 73 79
```

After knew what those loop does, i create python script to reverse the rot value.

**solver.py**

~~~python
#!/usr/bin/env python3
from string import ascii_lowercase, ascii_uppercase
def rot_n(a1, a2):
    ASCII_UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    ASCII_LOWER = "abcdefghijklmnopqrstuvwxyz"
    if ( chr(a1) in ASCII_UPPER):
        return ASCII_UPPER[(a2 + a1 - 65) % 26];
    if ( chr(a1) in ASCII_LOWER):
        return ASCII_LOWER[(a2 + a1 - 97) % 26];
    return chr(a1);

def main():
    flag = "ujp?_oHy_lxiu_zx_uve"
    prime = [2,5,11,13,17,23,29,29,37,37,41,47,53,53,59,61,67,71,73,79]
    for idx, val in enumerate(prime):
        print(rot_n(ord(flag[idx]), -val), end="")

if __name__ == '__main__':
    main()
~~~

```
➜  babyrev git:(master) ✗ python3 solve.py
see?_rEv_aint_so_bad
```



**FLAG:** corctf{see?_rEv_aint_so_bad}