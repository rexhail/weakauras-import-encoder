# Auras

Ready-to-use import strings for a TBC Anniversary Paladin.

## How to import

1. In game, type `/wa` to open WeakAuras.
2. Click **Import**.
3. Paste the full contents of a `.import.txt` file (Ctrl+V) and confirm.

Everything imports as a single group you can drag around as one piece. The Ret
and Prot groups each only load in their own spec (Ret checks for Crusader Strike,
Prot checks for Holy Shield), so they stay out of each other's way when you swap.

## rexhail-rotation-ret.import.txt  (adaptive Ret + Prot HUD)  — current (v3.2.1)

An adaptive rotation HUD. One import that auto-adapts to your spec, to what you
**know** (not your level), and to PvP vs PvE — Ret and Prot, leveling to 70.

**The press-now icon** is the standout: it's **bigger** than the rest and **flashes
bright gold the instant the global cooldown ends**, so you feel exactly when to
press (the "heartbeat"). A GCD bar and swing timer sit underneath.

**Retribution adapts in two tiers** (detected by which spells you know):

- **Tier A — leveling:** keep your seal up, then Judgement, Crusader Strike (once you
  have it), Hammer of Wrath under 20%, with Consecration (4+ enemies) and Exorcism
  (Undead/Demon) as fillers. Blessing and Paladin aura jump to the front when missing.
- **Tier B — twisting (~70, once you know Seal of Command + Seal of Blood/Martyr):** a
  swing-synced **twist track** appears above the row — ride the swing and twist your
  seal in the last 0.4s, building a combo. Judgement greys out unless your twist seal
  is up. (TBC has no native swing-timer API, so the 0.4s window is latency-compensated
  — a guide, ~0.1s jitter, same as every twist tool.)

**Protection** loads in a Prot build with its own threat priority: Righteous Fury,
Blessing of Sanctuary, Devotion Aura, Holy Shield, Avenger's Shield, Consecration
(always off cd), Judgement, then Hammer of Wrath / Exorcism.

**Status icon (right of the row):** shows your weapon — and in **1H+shield it shows
the shield**, so a glance tells you you're in shield mode. When you should be swinging
but aren't, it turns into a **red NOT-ATTACKING** warning in the same spot.

**Carried over:** at most 3 icons, left-anchored; a ~2.5s pre-ready sweep with a
sparkle the instant an ability comes up; a standalone seal indicator (grey + red when
no seal); mana-awareness (hides what you can't afford, resolved by highest known rank);
Crusader Strike drops while disarmed. One flat group, moves as one piece.

### Macros (Horde shown; Alliance: Seal of Blood → Seal of the Martyr)

```
# base seal — rank 1 (the per-swing proc is the same every rank, saves mana)
#showtooltip Seal of Command(Rank 1)
/cast Seal of Command(Rank 1)

# twist + start attacking
#showtooltip Seal of Blood
/cast Seal of Blood
/startattack

# Crusader Strike (instant, won't clip a seal cast)
#showtooltip Crusader Strike
/stopcasting
/cast Crusader Strike

# Judgement, then re-seal Command
#showtooltip Judgement
/startattack
/cast Judgement
/cast Seal of Command(Rank 1)

# opener — do NOT auto-attack while you set up seals
/stopattack
/cast Seal of the Crusader

# burst (with trinkets)
#showtooltip Avenging Wrath
/cast Avenging Wrath
/use 13
/use 14
```

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
