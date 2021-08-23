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