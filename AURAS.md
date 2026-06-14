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

## ret-priority-queue.import.txt  (Retribution)

A rotation **priority helper** — instead of static reminders, it shows a live row
of icons where the **leftmost icon is what to press right now**, and the rest sit
behind it dimmed, in priority order. As cooldowns, your seal, and the target's
health change, the icons reorder themselves on the fly.

The priority it follows (single target, built for leveling Ret):

1. **Seal of Command** — jumps to the front whenever no seal is up (no seal, no
   damage), so you always refresh it first.
2. **Hammer of Wrath** — slots in ahead of everything else once the target drops
   to 20% health or below (the execute window).
3. **Crusader Strike** — the 6s metronome the rotation is built on.
4. **Judgement** — woven in off the global cooldown.

When everything is on cooldown the row is empty, which simply means "keep
auto-attacking." Two details make it feel right in the hand: it ignores the
1.5s global cooldown when deciding what's ready (so the next button shows up
*during* the GCD, ready to queue, instead of leaving a dead gap), and the engine
re-evaluates every frame so an ability appears the exact instant it lights up on
your action bar — no lag.

It's a single icon driven by one custom trigger (a TSU that emits one state per
ready ability with a sort priority), arranged by a dynamic group sorted on that
priority. Inspired by the way Hekili-style and WotLK Death Knight rotation
WeakAuras present a reordering "what to press next" queue.

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
