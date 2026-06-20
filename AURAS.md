# Auras

Ready-to-use import strings for a TBC Anniversary Paladin.

## How to import

1. In game, type `/wa` to open WeakAuras.
2. Click **Import**.
3. Paste the full contents of a `.import.txt` file (Ctrl+V) and confirm.

Everything imports as a single group you can drag around as one piece. The Ret
and Prot groups each only load in their own spec (Ret checks for Crusader Strike,
Prot checks for Holy Shield), so they stay out of each other's way when you swap.

## rexhail-rotation-ret.import.txt  (Ret + Prot dual-spec)  — current (v2.3.0)

A rotation **priority helper**. Instead of static reminders it shows a live row
of icons where the **leftmost icon is what to press right now**, with a GCD bar
and a swing timer underneath. As cooldowns, your seal, and the target's health
change, the row updates and re-centers itself on the fly.

Since v2.0.0 it is **dual-spec**: the same group carries both a Retribution and a
Protection priority queue, and only the one for your current build loads (gated on
Crusader Strike for Ret, Holy Shield for Prot). Respec and it switches itself; the
GCD bar and swing timer are shared by both.

Retribution priority (single target):

1. **Blessing** — jumps to the front whenever no blessing is up.
2. **Sanctity Aura** — shown whenever no Paladin aura is active.
3. **Hammer of Wrath** — slots in once the target is at 20% health or below.
4. **Judgement** — top of the active rotation (v2.3.0: above Crusader Strike).
5. **Crusader Strike** — the 6s metronome the rotation is built on.
6. **Seal** — shown only when no seal is up; sits behind Judgement and Crusader
   Strike (v2.3.0) so re-sealing never bumps your damage buttons off the front.
7. **Exorcism** — a low-priority filler, only shown against Undead and Demon
   targets.

Protection priority (threat):

1. **Righteous Fury** — front whenever the threat buff is missing.
2. **Blessing of Sanctuary** — front whenever no blessing is up.
3. **Devotion Aura** — shown whenever no Paladin aura is active.
4. **Holy Shield** — the top active; recast on cooldown to keep block + threat up.
5. **Avenger's Shield** — off cooldown (pull / ranged threat).
6. **Consecration** — core threat, shown whenever it's off cooldown (always, not
   gated on enemy count like the Ret AoE hint).
7. **Judgement**, woven in off the global cooldown.
8. **Seal of Righteousness** — shown only when no seal is up; sits behind the
   active threat rotation (v2.3.0) rather than at the front.
9. **Hammer of Wrath** (execute) and **Exorcism** (Undead/Demon) as the
   lowest-priority fillers.

The row stays centered over the bars and **shows at most 3 icons at once**
(v2.3.0) — what to press now plus the next two — so it never sprawls into a busy
wall of icons. Built as one flat group (no nested groups), so it imports cleanly
and moves as one piece.

**Seal indicator (v2.1.0):** a small standalone icon next to the row always shows
your **current seal** in full colour. When no seal is up it goes grey with a red
glow, falling back to the last offensive seal you used — so you can see your seal
status at a glance without it ever taking a rotation slot.

**Seal & blessing managers:** it recognises any active seal and blessing (incl.
Greater blessings), so it never nags while one is up. The **seal** is only ever
suggested when you have *none* — and it remembers the last **offensive** seal you
cast (it ignores Seal of Wisdom/Light), so an opener like Seal of Wisdom → Seal of
Command doesn't confuse it (v2.1.0). The **blessing** is likewise only suggested
when you have none at all: Blessing of Might normally, or Blessing of Wisdom while
your mana is low — it never nags you to swap a blessing you already have up.

**Aura awareness:** Sanctity Aura is only suggested when no Paladin aura
(Devotion, Retribution, Concentration, the Resistance auras, Crusader, Sanctity)
is active.

**Pre-ready preview:** cooldown abilities appear in the row ~2.5s before they come
off cooldown (v2.0.0; was 1.5s), carrying a native radial cooldown swipe that fills
back to full colour exactly as they become usable — so you can line up the next
press on the beat. The instant an ability becomes usable it gives a small sparkle.
Ready abilities and reminders show in full colour with no swipe.

**GCD on the press-now icon (v2.0.0):** the leftmost "press now" icon shows the
global cooldown ticking down as a depleting sweep and brightens the instant the
GCD ends, so you can feel exactly when the next press lands. Only the top icon
carries it; the rest of the row stays clean.

**Usability & AoE (v1.5.0):** anything you can't currently afford the mana for is
hidden, and Crusader Strike drops out while you're disarmed (it's a weapon attack,
so it can't be used — Judgement and Exorcism stay). **Consecration** is added as an
AoE suggestion (after Judgement, before Exorcism): it only shows when there are 4+
enemies in range (roughly Consecration's radius), so it stays out of the way in
single target. Counting enemies needs enemy nameplates enabled.

**Mana-gate rank fix (v1.5.1):** the "can't afford the mana" check now resolves the
spell by name, i.e. the highest rank you actually have on your bar — so Exorcism,
Hammer of Wrath and your blessing no longer linger in the queue just because their
cheap rank 1 is affordable.

The seal and blessing handling above is shared by both specs, so swapping
Ret ↔ Prot needs no extra thought — the queue just switches with you.

Published on wago: https://wago.io/f-ofmKAvL

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
