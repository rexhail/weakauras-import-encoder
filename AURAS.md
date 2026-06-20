# Auras

Ready-to-use import strings for a TBC Anniversary Paladin.

## How to import

1. In game, type `/wa` to open WeakAuras.
2. Click **Import**.
3. Paste the full contents of a `.import.txt` file (Ctrl+V) and confirm.

Everything imports as a single group you can drag around as one piece. The Ret
and Prot groups each only load in their own spec (Ret checks for Crusader Strike,
Prot checks for Holy Shield), so they stay out of each other's way when you swap.

## rexhail-rotation-ret.import.txt  (Ret + Prot dual-spec)  — current (v2.6.0)

A rotation **priority helper**. Instead of static reminders it shows a live row
of icons where the **leftmost icon is what to press right now**, with a GCD bar
and a swing timer underneath. As cooldowns, your seal, and the target's health
change, the row updates on the fly, anchored to the left so the press-now icon
stays in one place.

Since v2.0.0 it is **dual-spec**: the same group carries both a Retribution and a
Protection priority queue, and only the one for your current build loads (gated on
Crusader Strike for Ret, Holy Shield for Prot). Respec and it switches itself; the
GCD bar and swing timer are shared by both.

Retribution priority (single target):

1. **Blessing** — jumps to the front whenever no blessing is up.
2. **Sanctity Aura** — shown whenever no Paladin aura is active.
3. **Hammer of Wrath** — slots in once the target is at 20% health or below.
4. **Judgement** — top of the active rotation (v2.3.0: above Crusader Strike). It
   greys out while you have no seal up, since it needs one to fire (v2.4.0).
5. **Crusader Strike** — the 6s metronome the rotation is built on.
6. **Exorcism** — a low-priority filler, only shown against Undead and Demon
   targets.

The seal is **not** in the rotation queue (removed v2.5.0) — the standalone seal
indicator and the greyed-out Judgement are your "you need a seal" cues instead.

Protection priority (threat):

1. **Righteous Fury** — front whenever the threat buff is missing.
2. **Blessing of Sanctuary** — front whenever no blessing is up.
3. **Devotion Aura** — shown whenever no Paladin aura is active.
4. **Holy Shield** — the top active; recast on cooldown to keep block + threat up.
5. **Avenger's Shield** — off cooldown (pull / ranged threat).
6. **Consecration** — core threat, shown whenever it's off cooldown (always, not
   gated on enemy count like the Ret AoE hint).
7. **Judgement**, woven in off the global cooldown (greys out with no seal up).
8. **Hammer of Wrath** (execute) and **Exorcism** (Undead/Demon) as the
   lowest-priority fillers.

The row is **anchored to the left** (v2.6.0): the press-now icon stays in one spot
and the next icons fill rightward, so there's no empty gap when only one or two
are queued. It **shows at most 3 icons at once** (v2.2.0) — what to press now plus
the next two. Built as one flat group (no nested groups), so it imports cleanly
and moves as one piece.

**Seal cues (v2.1.0 + v2.4.0):** a small standalone Seal Indicator next to the row
always shows your **current seal** in full colour; when no seal is up it goes grey
with a red glow, remembering the last offensive seal you used. On top of that, the
**Judgement** icon in the row greys out whenever you have no seal (v2.4.0) — so a
missing seal reads from two places. The seal itself is **not** suggested as a
rotation icon (removed v2.5.0); these two cues replace it.

**Blessing manager:** it recognises any active blessing (incl. Greater blessings),
so it never nags while one is up. The blessing is only suggested when you have none
at all: Blessing of Might normally, or Blessing of Wisdom while your mana is low —
it never nags you to swap a blessing you already have up.

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

The blessing handling and seal cues above are shared by both specs, so swapping
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
