# Auras

Ready-to-use import strings for a TBC Anniversary Retribution Paladin.

## How to import

1. In game, type `/wa` to open WeakAuras.
2. Click **Import**.
3. Paste the full contents of a `.import.txt` file (Ctrl+V) and confirm.

Everything imports as a single group you can drag around as one piece.

## ret-reminder-v3.1.import.txt

A focused reminder set, centered slightly below the middle of the screen:

- **Seal of Command** — always visible with remaining buff time; turns red and
  flashes when it drops, so you don't forget to refresh it.
- **Crusader Strike** — always visible with its cooldown counting down; flares
  gold the moment it's ready (it's the 6s metronome the rotation is built on).
- **Judgement** — same treatment; cast it on cooldown (it costs no global
  cooldown) to keep Judgement of the Crusader up.
- **Swing timer** — a bar with a tick marking the seal-twist window.
- **GCD bar** — a thin bar showing the global cooldown so you stop clipping it.
- **Hammer of Wrath** — hidden until the target is at 20% health or below, then
  it pops up as a glowing finisher.

The GCD bar and Hammer of Wrath use small custom triggers; everything else uses
native WeakAuras triggers.

## seal-tracker.import.txt

A single icon that shows your current seal and its remaining time, greyed out
when no seal is up. A simpler alternative if you only want seal tracking.
