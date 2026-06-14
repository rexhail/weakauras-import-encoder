# Auras

Ready-to-use import strings for a TBC Anniversary Paladin.

## How to import

1. In game, type `/wa` to open WeakAuras.
2. Click **Import**.
3. Paste the full contents of a `.import.txt` file (Ctrl+V) and confirm.

Everything imports as a single group you can drag around as one piece. The Ret
and Prot groups each only load in their own spec (Ret checks for Crusader Strike,
Prot checks for Holy Shield), so they stay out of each other's way when you swap.

## ret-reminder-v3.2.import.txt  (Retribution)

A focused reminder set, centered slightly below the middle of the screen.
Loads only while you're Retribution.

- **Seal of Command** — always visible with remaining buff time; turns red and
  flashes when it drops, so you don't forget to refresh it.
- **Crusader Strike** — always visible with its cooldown counting down; flares
  gold the moment it's ready (it's the 6s metronome the rotation is built on).
- **Judgement** — same treatment; cast it on cooldown to keep Judgement of the
  Crusader up.
- **Swing timer** — a bar with a green tick marking the 0.4s seal-twist window.
- **GCD bar** — a thin bar showing the global cooldown so you stop clipping it.
- **Hammer of Wrath** — hidden until the target is at 20% health or below, then
  it pops up as a glowing finisher.

The GCD bar and Hammer of Wrath use small custom triggers; everything else uses
native WeakAuras triggers.

## prot-reminder-v1.import.txt  (Protection)

A tank version. Loads only while you're Protection.

- **Seal (any)** — shows whichever seal is active and its remaining time; turns
  red and flashes when no seal is up.
- **Holy Shield** — stays bright while the buff is up and shows the remaining
  charges as a number; goes grey when it drops. The gold "recast" glow only
  fires once the spell is actually off cooldown, so it never tells you to recast
  while it's still on cooldown.
- **Avenger's Shield** — cooldown with a gold glow when it's ready.

## seal-tracker.import.txt

A single icon that shows your current seal and its remaining time, greyed out
when no seal is up. A simpler alternative if you only want seal tracking.
