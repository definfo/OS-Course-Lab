# OS-Course-Lab

## Lab0

Ref: [GDB Manual](https://ftp.gnu.org/old-gnu/Manuals/gdb/html_chapter/gdb_9.html#SEC51)

AArch64 Registers:

x29 - caller frame pointer
x30 - return address

```sh
nix shell nixpkgs#pkgsCross.aarch64-multiplatform.binutils # objdump

objdump -dS ./bomb
# ...

make qemu-gdb && make gdb


(gdb) disas main
# Dump of assembler code for function main:
#    0x0000000000400694 <+0>:     stp     x29, x30, [sp, #-16]!
#    0x0000000000400698 <+4>:     mov     x29, sp
#    0x000000000040069c <+8>:     adrp    x0, 0x464000 <free_mem+64>
#    0x00000000004006a0 <+12>:    add     x0, x0, #0x778
#    0x00000000004006a4 <+16>:    bl      0x413b20 <puts>
#    0x00000000004006a8 <+20>:    bl      0x400b10 <read_line>
#    0x00000000004006ac <+24>:    bl      0x400734 <phase_0>
#    0x00000000004006b0 <+28>:    bl      0x400708 <phase_defused>
#    0x00000000004006b4 <+32>:    bl      0x400b10 <read_line>
#    0x00000000004006b8 <+36>:    bl      0x400760 <phase_1>
#    0x00000000004006bc <+40>:    bl      0x400708 <phase_defused>
#    0x00000000004006c0 <+44>:    bl      0x400b10 <read_line>
#    0x00000000004006c4 <+48>:    bl      0x400788 <phase_2>
#    0x00000000004006c8 <+52>:    bl      0x400708 <phase_defused>
#    0x00000000004006cc <+56>:    bl      0x400b10 <read_line>
#    0x00000000004006d0 <+60>:    bl      0x400800 <phase_3>
#    0x00000000004006d4 <+64>:    bl      0x400708 <phase_defused>
#    0x00000000004006d8 <+68>:    bl      0x400b10 <read_line>
#    0x00000000004006dc <+72>:    bl      0x4009e4 <phase_4>
#    0x00000000004006e0 <+76>:    bl      0x400708 <phase_defused>
#    0x00000000004006e4 <+80>:    bl      0x400b10 <read_line>
#    0x00000000004006e8 <+84>:    bl      0x400ac0 <phase_5>
#    0x00000000004006ec <+88>:    bl      0x400708 <phase_defused>
#    0x00000000004006f0 <+92>:    adrp    x0, 0x464000 <free_mem+64>
#    0x00000000004006f4 <+96>:    add     x0, x0, #0x798
#    0x00000000004006f8 <+100>:   bl      0x413b20 <puts>
#    0x00000000004006fc <+104>:   mov     w0, #0x0                        // #0
#    0x0000000000400700 <+108>:   ldp     x29, x30, [sp], #16
#    0x0000000000400704 <+112>:   ret
# End of assembler dump.
```

---

```sh
(gdb) disas phase_0
# Dump of assembler code for function phase_0:
#    0x0000000000400734 <+0>:     stp     x29, x30, [sp, #-16]!
#    0x0000000000400738 <+4>:     mov     x29, sp
#    0x000000000040073c <+8>:     bl      0x400bd4 <read_int>
#    0x0000000000400740 <+12>:    adrp    x1, 0x4a0000
#    0x0000000000400744 <+16>:    ldr     w1, [x1, #84]
#    0x0000000000400748 <+20>:    cmp     w1, w0
#    0x000000000040074c <+24>:    b.ne    0x400758 <phase_0+36>  // b.any
#    0x0000000000400750 <+28>:    ldp     x29, x30, [sp], #16
#    0x0000000000400754 <+32>:    ret
#    0x0000000000400758 <+36>:    bl      0x400af4 <explode>
#    0x000000000040075c <+40>:    b       0x400750 <phase_0+28>
# End of assembler dump.
```

- The function calls `read_int()` which parses the user input and returns an int in `w0`.
- It loads a 32-bit value from memory (address computed via `adrp x1 + #84`) into `w1`.
- It compares `w1` with `w0`. If they are equal, the phase passes; otherwise it calls explode.
- Therefore the required input is the decimal integer equal to the 32-bit value stored at that memory location.

Solution: Extract the 32-bit integer value at address (0x4a0000 + 84).

```sh
(gdb) x/wd (0x4a0000 + 84) # Print as 32-bit decimal value
# 0x4a0054 <phase0_ans>:  2022
```

---

```sh
(gdb) disas phase_1
# Dump of assembler code for function phase_1:
#    0x0000000000400760 <+0>:     stp     x29, x30, [sp, #-16]!
#    0x0000000000400764 <+4>:     mov     x29, sp
#    0x0000000000400768 <+8>:     adrp    x1, 0x4a0000
#    0x000000000040076c <+12>:    ldr     x1, [x1, #88]
#    0x0000000000400770 <+16>:    bl      0x421b80 <strcmp>
#    0x0000000000400774 <+20>:    cbnz    w0, 0x400780 <phase_1+32>
#    0x0000000000400778 <+24>:    ldp     x29, x30, [sp], #16
#    0x000000000040077c <+28>:    ret
#    0x0000000000400780 <+32>:    bl      0x400af4 <explode>
#    0x0000000000400784 <+36>:    b       0x400778 <phase_1+24>
# End of assembler dump.
```

- TODO

Solution: Extract the string value from 64-bit pointer at address (0x4a0000 + 88).

```sh
(gdb) x/gx (0x4a0000 + 88) # Print as 64-bit hexadecimal value
# 0x4a0058 <phase1_ans>:  0x0000000000464810
(gdb) x/s 0x0000000000464810 # Print as string value
# 0x464810:       "KISS: Keep It Simple, Stupid."
```

---

```sh
(gdb) disas phase_2
# Dump of assembler code for function phase_2:
#    0x0000000000400788 <+0>:     stp     x29, x30, [sp, #-64]!
#    0x000000000040078c <+4>:     mov     x29, sp
#    0x0000000000400790 <+8>:     stp     x19, x20, [sp, #16]
#    0x0000000000400794 <+12>:    add     x1, sp, #0x20
#    0x0000000000400798 <+16>:    bl      0x400b7c <read_8_numbers>
#    0x000000000040079c <+20>:    ldr     w0, [sp, #32]
#    0x00000000004007a0 <+24>:    cmp     w0, #0x1
#    0x00000000004007a4 <+28>:    b.ne    0x4007b4 <phase_2+44>  // b.any
#    0x00000000004007a8 <+32>:    ldr     w0, [sp, #36]
#    0x00000000004007ac <+36>:    cmp     w0, #0x1
#    0x00000000004007b0 <+40>:    b.eq    0x4007b8 <phase_2+48>  // b.none
#    0x00000000004007b4 <+44>:    bl      0x400af4 <explode>
#    0x00000000004007b8 <+48>:    add     x19, sp, #0x20
#    0x00000000004007bc <+52>:    add     x20, sp, #0x38
#    0x00000000004007c0 <+56>:    b       0x4007d0 <phase_2+72>
#    0x00000000004007c4 <+60>:    add     x19, x19, #0x4
#    0x00000000004007c8 <+64>:    cmp     x19, x20
#    0x00000000004007cc <+68>:    b.eq    0x4007f4 <phase_2+108>  // b.none
#    0x00000000004007d0 <+72>:    ldr     w0, [x19]
#    0x00000000004007d4 <+76>:    ldr     w1, [x19, #4]
#    0x00000000004007d8 <+80>:    add     w0, w0, w1
#    0x00000000004007dc <+84>:    add     w0, w0, #0x4
#    0x00000000004007e0 <+88>:    ldr     w1, [x19, #8]
#    0x00000000004007e4 <+92>:    cmp     w1, w0
#    0x00000000004007e8 <+96>:    b.eq    0x4007c4 <phase_2+60>  // b.none
#    0x00000000004007ec <+100>:   bl      0x400af4 <explode>
#    0x00000000004007f0 <+104>:   b       0x4007c4 <phase_2+60>
#    0x00000000004007f4 <+108>:   ldp     x19, x20, [sp, #16]
#    0x00000000004007f8 <+112>:   ldp     x29, x30, [sp], #64
#    0x00000000004007fc <+116>:   ret
# End of assembler dump. 

(gdb) disas 0x400b7c
# Dump of assembler code for function read_8_numbers:
#    0x0000000000400b7c <+0>:     sub     sp, sp, #0x20 /// Allocate stack frame (32-byte)
#    0x0000000000400b80 <+4>:     stp     x29, x30, [sp, #16] /// Save callee-saved regs x29/x30 at [$sp + 16]/[$sp + 12]
#    0x0000000000400b84 <+8>:     add     x29, sp, #0x10 /// Update stack frame pointer

#    0x0000000000400b88 <+12>:    mov     x2, x1 /// Copy x1 (note base_addr) into x2; x2 = base_addr
#    0x0000000000400b8c <+16>:    add     x1, x1, #0x1c /// x1 = base_addr + 28
#    0x0000000000400b90 <+20>:    str     x1, [sp, #8] /// Store (base_addr + 28) at [$sp + 8]
#    0x0000000000400b94 <+24>:    add     x1, x2, #0x18 /// x1 = base_addr + 24
#    0x0000000000400b98 <+28>:    str     x1, [sp] /// Store (base_addr + 24) at [$sp]
#    0x0000000000400b9c <+32>:    add     x7, x2, #0x14 /// x7 = base_addr + 20
#    0x0000000000400ba0 <+36>:    add     x6, x2, #0x10 /// x6 = base_addr + 16
#    0x0000000000400ba4 <+40>:    add     x5, x2, #0xc /// x5 = base_addr + 12
#    0x0000000000400ba8 <+44>:    add     x4, x2, #0x8 /// x4 = base_addr + 8
#    0x0000000000400bac <+48>:    add     x3, x2, #0x4 /// x3 = base_addr + 4
#    0x0000000000400bb0 <+52>:    adrp    x1, 0x464000 <free_mem+64>
#    0x0000000000400bb4 <+56>:    add     x1, x1, #0x838 /// Load format string into x1; x1 = "%d %d %d %d %d %d %d %d"
#                                                        /// (gdb) x/s (0x464000 + 0x838)
#                                                        /// 0x464838:       "%d %d %d %d %d %d %d %d"
#    0x0000000000400bb8 <+60>:    bl      0x406d80 <__isoc99_sscanf> /// Call sscanf

#    0x0000000000400bbc <+64>:    cmp     w0, #0x7
#    0x0000000000400bc0 <+68>:    b.le    0x400bd0 <read_8_numbers+84> /// Explode if w0 <= 7 (incorrect number of arguments)

#    0x0000000000400bc4 <+72>:    ldp     x29, x30, [sp, #16] /// Restore callee-saved regs x29/x30
#    0x0000000000400bc8 <+76>:    add     sp, sp, #0x20 /// Release stack frame
#    0x0000000000400bcc <+80>:    ret

#    0x0000000000400bd0 <+84>:    bl      0x400af4 <explode>
# End of assembler dump.
```

- Read 8 numbers with `sscanf(?, x1, x2, x3, x4, x5, x6, x7, $sp, $sp + 8)`
- In caller (phase_2), `read_8_numbers::base_addr = phase_2::$sp + 32`
- `w0 = *x2`, explode if `w0 != 1`
- `w0 = *x3`, explode if `w0 != 1`
- `w0 = x[i]`
  `w1 = x[i+1]`
  `w0 = x[i] + x[i+1]`
  `w0 = w0 + 4`
  `w1 = x[i+2]`
  
  explode if `x[i+2] != x[i] + x[i+1] + 4`

Solution:

1
1
1 + 1 + 4 = 6
1 + 6 + 4 = 11
...

`1 1 6 11 21 36 61 101`

---

```sh
(gdb) disassemble phase_3
# Dump of assembler code for function phase_3:
#    0x0000000000400800 <+0>:     stp     x29, x30, [sp, #-32]!
#    0x0000000000400804 <+4>:     mov     x29, sp
#    0x0000000000400808 <+8>:     add     x3, sp, #0x18
#    0x000000000040080c <+12>:    add     x2, sp, #0x1c
# => 0x0000000000400810 <+16>:    adrp    x1, 0x464000 <free_mem+64>
#    0x0000000000400814 <+20>:    add     x1, x1, #0x7d8
#    0x0000000000400818 <+24>:    bl      0x406d80 <__isoc99_sscanf>
#    0x000000000040081c <+28>:    cmp     w0, #0x2
#    0x0000000000400820 <+32>:    b.ne    0x40084c <phase_3+76>  // b.any
#    0x0000000000400824 <+36>:    ldr     w0, [sp, #28]
#    0x0000000000400828 <+40>:    cmp     w0, #0x4
#    0x000000000040082c <+44>:    b.eq    0x400884 <phase_3+132>  // b.none
#    0x0000000000400830 <+48>:    cmp     w0, #0x7
#    0x0000000000400834 <+52>:    b.eq    0x4008a0 <phase_3+160>  // b.none
#    0x0000000000400838 <+56>:    cmp     w0, #0x2
#    0x000000000040083c <+60>:    b.eq    0x400854 <phase_3+84>  // b.none
#    0x0000000000400840 <+64>:    bl      0x400af4 <explode>
#    0x0000000000400844 <+68>:    ldp     x29, x30, [sp], #32
#    0x0000000000400848 <+72>:    ret
#    0x000000000040084c <+76>:    bl      0x400af4 <explode>
#    0x0000000000400850 <+80>:    b       0x400824 <phase_3+36>
#    0x0000000000400854 <+84>:    ldr     w2, [sp, #24]
#    0x0000000000400858 <+88>:    mov     w0, #0x6667                     // #26215
#    0x000000000040085c <+92>:    movk    w0, #0x6666, lsl #16
#    0x0000000000400860 <+96>:    smull   x0, w2, w0
#    0x0000000000400864 <+100>:   asr     x0, x0, #34
#    0x0000000000400868 <+104>:   sub     w0, w0, w2, asr #31
#    0x000000000040086c <+108>:   add     w1, w0, w0, lsl #2
#    0x0000000000400870 <+112>:   sub     w1, w2, w1, lsl #1
#    0x0000000000400874 <+116>:   add     w0, w1, w0
#    0x0000000000400878 <+120>:   cmp     w0, #0x2
#    0x000000000040087c <+124>:   b.eq    0x400844 <phase_3+68>  // b.none
#    0x0000000000400880 <+128>:   bl      0x400af4 <explode>
#    0x0000000000400884 <+132>:   ldr     w0, [sp, #24]
#    0x0000000000400888 <+136>:   eor     w0, w0, w0, asr #3
#    0x000000000040088c <+140>:   and     w0, w0, #0x7
#    0x0000000000400890 <+144>:   ldr     w1, [sp, #28]
#    0x0000000000400894 <+148>:   cmp     w0, w1
#    0x0000000000400898 <+152>:   b.eq    0x400844 <phase_3+68>  // b.none
#    0x000000000040089c <+156>:   bl      0x400af4 <explode>
#    0x00000000004008a0 <+160>:   ldr     w0, [sp, #24]
#    0x00000000004008a4 <+164>:   ldr     w1, [sp, #28]
#    0x00000000004008a8 <+168>:   and     w2, w0, #0x7
#    0x00000000004008ac <+172>:   cmp     w2, w1
#    0x00000000004008b0 <+176>:   b.eq    0x400844 <phase_3+68>  // b.none
#    0x00000000004008b4 <+180>:   ubfx    x0, x0, #3, #3
#    0x00000000004008b8 <+184>:   cmp     w1, w0
#    0x00000000004008bc <+188>:   b.eq    0x400844 <phase_3+68>  // b.none
#    0x00000000004008c0 <+192>:   bl      0x400af4 <explode>
#    0x00000000004008c4 <+196>:   b       0x400840 <phase_3+64>
# End of assembler dump.
```

```c
int a, b;
if (sscanf(input, "%d %d", &a, &b) != 2)
    explode();

switch (a) {
case 2: // a = 2
    if ((b / 10 + b % 10) != 2) // b = 2, 11, 20
        explode();
    break;

case 4: // a = 4
    if (((b ^ (b >> 3)) & 7) != a) // b = 4
        explode();
    break;

case 7: // a = 7
    if ((b & 7) == a) // b = 7
        break;
    if (((b >> 3) & 7) == 7) // b = 56
        break;
    explode();
    break;

default:
    explode();
}
return;
```

Solution (One of the following):

`2 2`, `2 11`, `2 20`, `4 4`, `7 7`, `7 56`

---

```sh
(gdb) disassemble phase_4
# Dump of assembler code for function phase_4:
#    0x00000000004009e4 <+0>:     stp     x29, x30, [sp, #-32]!
#    0x00000000004009e8 <+4>:     mov     x29, sp
#    0x00000000004009ec <+8>:     stp     x19, x20, [sp, #16]
#    0x00000000004009f0 <+12>:    mov     x19, x0
# => 0x00000000004009f4 <+16>:    bl      0x400300
#    0x00000000004009f8 <+20>:    mov     x20, x0
#    0x00000000004009fc <+24>:    cmp     w0, #0xa
#    0x0000000000400a00 <+28>:    b.gt    0x400a3c <phase_4+88>
#    0x0000000000400a04 <+32>:    mov     w1, w20
#    0x0000000000400a08 <+36>:    mov     x0, x19
#    0x0000000000400a0c <+40>:    bl      0x4008c8 <encrypt_method1>
#    0x0000000000400a10 <+44>:    mov     w1, w20
#    0x0000000000400a14 <+48>:    mov     x0, x19
#    0x0000000000400a18 <+52>:    bl      0x400964 <encrypt_method2>
#    0x0000000000400a1c <+56>:    adrp    x0, 0x4a0000
#    0x0000000000400a20 <+60>:    ldr     x1, [x0, #104]
#    0x0000000000400a24 <+64>:    mov     x0, x19
#    0x0000000000400a28 <+68>:    bl      0x421b80 <strcmp>
#    0x0000000000400a2c <+72>:    cbnz    w0, 0x400a44 <phase_4+96>
#    0x0000000000400a30 <+76>:    ldp     x19, x20, [sp, #16]
#    0x0000000000400a34 <+80>:    ldp     x29, x30, [sp], #32
#    0x0000000000400a38 <+84>:    ret
#    0x0000000000400a3c <+88>:    bl      0x400af4 <explode>
#    0x0000000000400a40 <+92>:    b       0x400a04 <phase_4+32>
#    0x0000000000400a44 <+96>:    bl      0x400af4 <explode>
#    0x0000000000400a48 <+100>:   b       0x400a30 <phase_4+76>
# End of assembler dump.

(gdb) disassemble encrypt_method1
# Dump of assembler code for function encrypt_method1:
#    0x00000000004008c8 <+0>:     stp     x29, x30, [sp, #-32]!
#    0x00000000004008cc <+4>:     mov     x29, sp
#    0x00000000004008d0 <+8>:     add     x2, sp, #0x10
#    0x00000000004008d4 <+12>:    strb    wzr, [x2, w1, sxtw]
#    0x00000000004008d8 <+16>:    add     w3, w1, w1, lsr #31
#    0x00000000004008dc <+20>:    asr     w3, w3, #1
#    0x00000000004008e0 <+24>:    cmp     w1, #0x1
#    0x00000000004008e4 <+28>:    b.le    0x40095c <encrypt_method1+148>
#    0x00000000004008e8 <+32>:    mov     x4, x2
#    0x00000000004008ec <+36>:    mov     x2, #0x0                        // #0
#    0x00000000004008f0 <+40>:    lsl     x5, x2, #1
#    0x00000000004008f4 <+44>:    ldrb    w5, [x0, x5]
#    0x00000000004008f8 <+48>:    strb    w5, [x4], #1
#    0x00000000004008fc <+52>:    add     x2, x2, #0x1
#    0x0000000000400900 <+56>:    cmp     w3, w2
#    0x0000000000400904 <+60>:    b.gt    0x4008f0 <encrypt_method1+40>
#    0x0000000000400908 <+64>:    cmp     w3, #0x0
#    0x000000000040090c <+68>:    csinc   w5, w3, wzr, gt
#    0x0000000000400910 <+72>:    cmp     w1, w5
#    0x0000000000400914 <+76>:    b.le    0x40094c <encrypt_method1+132>
#    0x0000000000400918 <+80>:    sub     w4, w1, w5
#    0x000000000040091c <+84>:    sub     w2, w5, w3
#    0x0000000000400920 <+88>:    add     x2, x0, w2, sxtw #1
#    0x0000000000400924 <+92>:    add     x2, x2, #0x1
#    0x0000000000400928 <+96>:    mov     x1, #0x0                        // #0
#    0x000000000040092c <+100>:   add     x3, sp, #0x10
#    0x0000000000400930 <+104>:   add     x5, x3, w5, sxtw
#    0x0000000000400934 <+108>:   lsl     x3, x1, #1
#    0x0000000000400938 <+112>:   ldrb    w3, [x2, x3]
#    0x000000000040093c <+116>:   strb    w3, [x5, x1]
#    0x0000000000400940 <+120>:   add     x1, x1, #0x1
#    0x0000000000400944 <+124>:   cmp     x1, x4
#    0x0000000000400948 <+128>:   b.ne    0x400934 <encrypt_method1+108>  // b.any
#    0x000000000040094c <+132>:   add     x1, sp, #0x10
#    0x0000000000400950 <+136>:   bl      0x421cc0 <strcpy>
#    0x0000000000400954 <+140>:   ldp     x29, x30, [sp], #32
#    0x0000000000400958 <+144>:   ret
#    0x000000000040095c <+148>:   mov     w5, #0x0                        // #0
#    0x0000000000400960 <+152>:   b       0x400910 <encrypt_method1+72>
# End of assembler dump.

(gdb) disassemble encrypt_method2
# Dump of assembler code for function encrypt_method2:
#    0x0000000000400964 <+0>:     cmp     w1, #0x0
#    0x0000000000400968 <+4>:     b.le    0x4009e0 <encrypt_method2+124>
#    0x000000000040096c <+8>:     stp     x29, x30, [sp, #-48]!
#    0x0000000000400970 <+12>:    mov     x29, sp
#    0x0000000000400974 <+16>:    stp     x19, x20, [sp, #16]
#    0x0000000000400978 <+20>:    stp     x21, x22, [sp, #32]
#    0x000000000040097c <+24>:    mov     x19, x0
#    0x0000000000400980 <+28>:    add     x21, x0, w1, sxtw
#    0x0000000000400984 <+32>:    adrp    x22, 0x4a0000
#    0x0000000000400988 <+36>:    add     x22, x22, #0x58
#    0x000000000040098c <+40>:    b       0x4009b0 <encrypt_method2+76>
#    0x0000000000400990 <+44>:    ldrb    w1, [x20]
#    0x0000000000400994 <+48>:    ldr     x0, [x22, #8]
#    0x0000000000400998 <+52>:    add     x0, x0, x1
#    0x000000000040099c <+56>:    ldurb   w0, [x0, #-97]
#    0x00000000004009a0 <+60>:    strb    w0, [x20]
#    0x00000000004009a4 <+64>:    add     x19, x19, #0x1
#    0x00000000004009a8 <+68>:    cmp     x19, x21
#    0x00000000004009ac <+72>:    b.eq    0x4009d0 <encrypt_method2+108>  // b.none
#    0x00000000004009b0 <+76>:    mov     x20, x19
#    0x00000000004009b4 <+80>:    ldrb    w0, [x19]
#    0x00000000004009b8 <+84>:    sub     w0, w0, #0x61
#    0x00000000004009bc <+88>:    and     w0, w0, #0xff
#    0x00000000004009c0 <+92>:    cmp     w0, #0x19
#    0x00000000004009c4 <+96>:    b.ls    0x400990 <encrypt_method2+44>  // b.plast
#    0x00000000004009c8 <+100>:   bl      0x400af4 <explode>
#    0x00000000004009cc <+104>:   b       0x400990 <encrypt_method2+44>
#    0x00000000004009d0 <+108>:   ldp     x19, x20, [sp, #16]
#    0x00000000004009d4 <+112>:   ldp     x21, x22, [sp, #32]
#    0x00000000004009d8 <+116>:   ldp     x29, x30, [sp], #48
#    0x00000000004009dc <+120>:   ret
#    0x00000000004009e0 <+124>:   ret
# End of assembler dump.
```

Inspect input:

```sh
(gdb) print $w0
# $1 = 10
(gdb) x/s $x19
# 0x4a2138 <input_buf>:   "<input_str>"
```

Probe runtime information:

```sh
(gdb) x/4gx 0x4a0058
# 0x4a0058 <phase1_ans>:  0x0000000000464810      0x00000000004647f0
# 0x4a0068 <expected_cipher>:     0x00000000004647e0      0x0000000000000031

(gdb) x/gx 0x4a0068
# 0x4a0068 <expected_cipher>:     0x00000000004647e0
(gdb) x/s *(char**)0x4a0068
# 0x4647e0:       "isggstsvke"

(gdb) x/gx 0x4a0060
# 0x4a0060 <dict>:        0x00000000004647f0
(gdb) set $tbl = *(void**)0x4a0060
(gdb) x/26cb $tbl
# 0x4647f0:       113 'q' 119 'w' 101 'e' 114 'r' 116 't' 121 'y' 117 'u' 105 'i'
# 0x4647f8:       111 'o' 112 'p' 97 'a'  115 's' 100 'd' 102 'f' 103 'g' 104 'h'
# 0x464800:       106 'j' 107 'k' 108 'l' 122 'z' 120 'x' 99 'c'  118 'v' 98 'b'
# 0x464808:       110 'n' 109 'm'
```

Solution:

- encryption_method2

  cipher ⇐ plaintext

  Expected cipher := "isggstsvke"
  Substitution table `<dict>` := "qwertyuiopasdfghjklzxcvbnm"
  
  "isggstsvke" ⇐ "hloolelwrc"

- encryption_method1

  `s[0,2,4,6,8,1,3,5,7,9]` ⇐ `char s[10]`
  
  "hloolelwrc" ⇐ "helloworlc`

---

```sh
(gdb) disas phase_5
# Dump of assembler code for function phase_5:
#    0x0000000000400ac0 <+0>:     stp     x29, x30, [sp, #-16]!
#    0x0000000000400ac4 <+4>:     mov     x29, sp
# => 0x0000000000400ac8 <+8>:     bl      0x400bd4 <read_int>
#    0x0000000000400acc <+12>:    adrp    x1, 0x4a0000
#    0x0000000000400ad0 <+16>:    add     x1, x1, #0x58
#    0x0000000000400ad4 <+20>:    add     x1, x1, #0x18
#    0x0000000000400ad8 <+24>:    bl      0x400a4c <func_5>
#    0x0000000000400adc <+28>:    cmp     w0, #0x3
#    0x0000000000400ae0 <+32>:    b.ne    0x400aec <phase_5+44>  // b.any
#    0x0000000000400ae4 <+36>:    ldp     x29, x30, [sp], #16
#    0x0000000000400ae8 <+40>:    ret
#    0x0000000000400aec <+44>:    bl      0x400af4 <explode>
#    0x0000000000400af0 <+48>:    b       0x400ae4 <phase_5+36>
# End of assembler dump.

(gdb) disas read_int
# Dump of assembler code for function read_int:
#    0x0000000000400bd4 <+0>:     stp     x29, x30, [sp, #-32]!
#    0x0000000000400bd8 <+4>:     mov     x29, sp
#    0x0000000000400bdc <+8>:     add     x2, sp, #0x1c
#    0x0000000000400be0 <+12>:    adrp    x1, 0x464000 <free_mem+64>
#    0x0000000000400be4 <+16>:    add     x1, x1, #0x850
#    0x0000000000400be8 <+20>:    bl      0x406d80 <__isoc99_sscanf>
#    0x0000000000400bec <+24>:    cmp     w0, #0x0
#    0x0000000000400bf0 <+28>:    b.le    0x400c00 <read_int+44>
#    0x0000000000400bf4 <+32>:    ldr     w0, [sp, #28]
#    0x0000000000400bf8 <+36>:    ldp     x29, x30, [sp], #32
#    0x0000000000400bfc <+40>:    ret
#    0x0000000000400c00 <+44>:    bl      0x400af4 <explode>
# End of assembler dump.

(gdb) disas func_5
# Dump of assembler code for function func_5:
#    0x0000000000400a4c <+0>:     cbz     x1, 0x400ab8 <func_5+108>
#    0x0000000000400a50 <+4>:     stp     x29, x30, [sp, #-32]!
#    0x0000000000400a54 <+8>:     mov     x29, sp
#    0x0000000000400a58 <+12>:    stp     x19, x20, [sp, #16]
#    0x0000000000400a5c <+16>:    mov     w20, w0
#    0x0000000000400a60 <+20>:    mov     x19, x1
#    0x0000000000400a64 <+24>:    ldr     w0, [x1]
#    0x0000000000400a68 <+28>:    cmp     w0, w20
#    0x0000000000400a6c <+32>:    b.eq    0x400a98 <func_5+76>  // b.none
#    0x0000000000400a70 <+36>:    ldr     w0, [x19]
#    0x0000000000400a74 <+40>:    cmp     w0, w20
#    0x0000000000400a78 <+44>:    b.le    0x400aa0 <func_5+84>
#    0x0000000000400a7c <+48>:    ldr     x1, [x19, #8]
#    0x0000000000400a80 <+52>:    mov     w0, w20
#    0x0000000000400a84 <+56>:    bl      0x400a4c <func_5>
#    0x0000000000400a88 <+60>:    lsl     w0, w0, #1
#    0x0000000000400a8c <+64>:    ldp     x19, x20, [sp, #16]
#    0x0000000000400a90 <+68>:    ldp     x29, x30, [sp], #32
#    0x0000000000400a94 <+72>:    ret
#    0x0000000000400a98 <+76>:    bl      0x400af4 <explode>
#    0x0000000000400a9c <+80>:    b       0x400a70 <func_5+36>
#    0x0000000000400aa0 <+84>:    ldr     x1, [x19, #16]
#    0x0000000000400aa4 <+88>:    mov     w0, w20
#    0x0000000000400aa8 <+92>:    bl      0x400a4c <func_5>
#    0x0000000000400aac <+96>:    lsl     w0, w0, #1
#    0x0000000000400ab0 <+100>:   add     w0, w0, #0x1
#    0x0000000000400ab4 <+104>:   b       0x400a8c <func_5+64>
#    0x0000000000400ab8 <+108>:   mov     w0, #0x0                        // #0
#    0x0000000000400abc <+112>:   ret
# End of assembler dump.
```

Find a top-down route on Binary Search Tree.

```sh
(gdb) x/wx 0x4a0070
# 0x4a0070 <search_tree>: 0x00000031
(gdb) x/gx 0x4a0070+16
# 0x4a0080 <search_tree+16>:      0x00000000004a00a0
(gdb) set $r = (char*)0x4a0070
(gdb) x/wx $r
# 0x4a0070 <search_tree>: 0x00000031
(gdb) x/gx $r+8
# 0x4a0078 <search_tree+8>:       0x00000000004a0088
(gdb) x/gx $r+16
# 0x4a0080 <search_tree+16>:      0x00000000004a00a0
(gdb) set $n1 = *(long*)($r+16)
(gdb) x/wx $n1
# 0x4a00a0 <search_tree+48>:      0x00000061
(gdb) x/gx $n1+8
# 0x4a00a8 <search_tree+56>:      0x00000000004a00e8
(gdb) x/gx $n1+16
# 0x4a00b0 <search_tree+64>:      0x00000000004a0100
(gdb) set $n2 = *(long*)($n1+16)
(gdb) x/wx $n2
# 0x4a0100 <search_tree+144>:     0x00000064
(gdb) x/gx $n2+8
# 0x4a0108 <search_tree+152>:     0x0000000000000000
(gdb) x/gx $n2+16
# 0x4a0110 <search_tree+160>:     0x0000000000000000
```

The required integer `x` should satisfy:
- `x > 0x31 (49)`
- `x > 0x61 (97)`
- `x < 0x64 (100)`

`98` or `99`
