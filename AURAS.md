# Auras

Ready-to-use import strings for a TBC Anniversary Paladin.

## How to import

1. In game, type `/wa` to open WeakAuras.
2. Click **Import**.
3. Paste the full contents of a `.import.txt` file (Ctrl+V) and confirm.

Everything imports as a single group you can drag around as one piece. The Ret
and Prot groups each only load in their own spec (Ret checks for Crusader Strike,
Prot checks for Holy Shield), so they stay out of each other's way when you swap.

## rexhail-rotation-ret.import.txt  (Ret + Prot dual-spec)  — current (v2.0.0)

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
3. **Seal** — front whenever no seal is up.
4. **Hammer of Wrath** — slots in once the target is at 20% health or below.
5. **Crusader Strike** — the 6s metronome the rotation is built on.
6. **Judgement** — woven in off the global cooldown.
7. **Exorcism** — a low-priority filler, only shown against Undead and Demon
   targets.

Protection priority (threat):

1. **Righteous Fury** — front whenever the threat buff is missing.
2. **Blessing of Sanctuary** — front whenever no blessing is up.
3. **Devotion Aura** — shown whenever no Paladin aura is active.
4. **Seal of Righteousness** — front whenever no seal is up.
5. **Holy Shield** — the top active; recast on cooldown to keep block + threat up.
6. **Avenger's Shield** — off cooldown (pull / ranged threat).
7. **Consecration** — core threat, shown whenever it's off cooldown (always, not
   gated on enemy count like the Ret AoE hint).
8. **Judgement**, then **Hammer of Wrath** (execute) and **Exorcism**
   (Undead/Demon) as the lowest-priority fillers.

The row stays centered over the bars no matter how many icons are visible. Built
as one flat group (no nested groups), so it imports cleanly and moves as one piece.

**Mana-aware seal & blessing managers:** it recognises any active seal and
blessing (incl. Greater blessings), so it never nags while one is up. When your
mana drops below 12% it suggests **Seal of Wisdom** as a soft hint, and once you
climb back above 40% it points you back to your offensive seal — remembering
whichever one you use, so it adapts to Seal of Blood/Martyr. The same applies to
**Blessing of Wisdom**, but only while you have no Blessing of Might up, so it
never nags you to swap mid-fight. If **Judgement of Wisdom** is already on the
target (yours or a group member's), the Seal of Wisdom hint stops and it points
you back to your offensive seal, since the mana is already covered. These hints
sit at the end of the queue and never block the rotation.

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

**Prot seal handling (v2.0.0):** in Protection the rotation never nags you to swap
seals while any seal is up (including Seal of Wisdom) — it only suggests a seal
when you have none, plus the low-mana Seal of Wisdom hint. (Retribution keeps
pointing you back to your offensive seal once your mana recovers.)

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
