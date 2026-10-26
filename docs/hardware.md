---
hide:
  - navigation
---

# Hardware

!!! note "In progress"
    This page collects the bench setup and the measurements of the bring-up. Sections
    marked *pending* are filled in from the captures in `evidence/hardware/`.

## Bench

| Node | Hardware | Firmware |
| --- | --- | --- |
| Master 0x01 | PC with a USB-UART adapter | `examples/host_serial` of Baton-C |
| Slave 0x12 | Microchip M2S010 MKR Kit (SmartFusion2, Cortex-M3 at 100 MHz) | `zephyr/samples/baton_node` |

## Wiring

All nodes share one line at 9600 bit/s, 8N1:

- **Open drain.** Each TX drives the line through an open-drain stage (or a diode with
  the cathode toward TX), each RX reads the line, one pull-up (for example 4.7 kΩ to
  3.3 V) holds the idle level.
- **RS-485.** Each node has a half-duplex transceiver whose receiver stays enabled while
  it transmits (RE tied low), so every node hears its own bytes; the driver enable is
  `de-gpios` in devicetree.

On SmartFusion2, the FPGA design (Libero SoC) routes MSS UART1 to the package pins; the
pins used on the MKR Kit are *pending*.

## Checklist of the measurements

- [ ] Wiring diagram and photo of the bench
- [ ] Logic-analyzer capture of one poll slot (POLL, DATA/ACK, RESP) with timing
- [ ] Measured cycle time against the cycle computed from the configuration
- [ ] Thread stack usage (`CONFIG_THREAD_ANALYZER`)
- [ ] Unplugging the slave: the master reports it, the event is reported undeliverable
- [ ] Noise on the line (for example a switched motor): CRC errors counted, no silent loss
