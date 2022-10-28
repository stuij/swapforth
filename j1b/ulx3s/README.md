The ULX3S board is based upon the Lattice ECP5 FPGA. It's a it's a prototype
board with lots of features in a small form factor. For more info, see
https://ulx3s.github.io.

Currently the only tested toolchain is Trellis (or rather the tools associated
with Trellis).

As with the other supported platforms, have the Trellis tools installed, and run
make in this directory to create a bitstream. Run fujprog to install it over
USB:

  fujprog ulx3s_85f_swapforth.bit

Now you can use `shell.py` in the parent directory to attach to the Forth
process over UART. The Verilator bootstrap process will also work for ULX3S.

Currently only J1b itself, UART, buttons and LEDs are supported. Support for
low-hanging fruit like GPIOs should follow shortly.


PWR button resets the board

memory map:

0x0400: buttons (excluding PWR)
direction: in
each button occupies one bit in the bottom 6 bits

as per silkscreen labels on the board:
|  32 - 6  |  5  |  4  |  3  |  2  |  1  |  0  |
 unused     RIGHT LEFT  DOWN  UP    F2    F1

example:

  $0400 io@ .



0x0404: leds
direction: out
each led occupies one bit in the bottom 8 bits

as per silkscreen labels on the board:
|  32 - 8 |  7  |  6  |  5  |  4  |  3  |  2  |  1  |  0  |
  unused    D7    D6    D5    D4    D3    D2    D1    D0

example:
  : led-counter     / interpret LEDs as a byte
    0 begin
      dup $0404 io! / write to LEDs, initially 0
      1+            / increment bits every loop
      200 ms        / wait for 1/5th of a second
    again
  ;
  led-counter
