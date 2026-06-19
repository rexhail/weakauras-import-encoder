# Design — Rexhail Rotation: dual-spec (Ret + Prot) v2.0.0

Date: 2026-06-19
Status: approved (brainstorming), pending implementation plan

## Goal

Extend the existing **Rexhail Rotation - Ret Paladin** WeakAura (TBC Anniversary
2.5.5, enUS) into a single dual-spec aura that helps both Retribution (DPS) and
Protection (tank). The Ret behaviour must stay byte-identical; Prot gets its own
priority queue, shown only while in a Protection build.

## Architecture — one flat group, slots gated per spec

A single import string / single flat group (no nested groups — they don't survive
import on TBC Anniversary). Children:

- **9 Ret icon slots** — uids `RexhailRet_s1..s9` (unchanged trigger logic). Add a
  load gate `use_spellknown=true, spellknown=35395` (Crusader Strike) so they load
  **only in a Ret build**. This touches the slots' `load` table only, never the
  trigger custom code.
- **9 Prot icon slots** — new uids `RexhailProt_s1..s9`. Same 9 fixed screen
  positions (xOffset −116,−87,−58,−29,0,29,58,87,116; y=−150; step 29px; SCREEN/
  CENTER), same icon size, same visual machinery (pre-ready cooldown sweep,
  ACShine sparkle on ready, centering formula, cap-to-5). Load gate
  `use_spellknown=true, spellknown=20925` (Holy Shield) → loads **only in a Prot
  build**. New TSU custom code with the Prot priority queue.
- **GCD bar** (`RexhailRet_gcd`) and **Swing timer** (`RexhailRet_swing`) — stay
  `class=PALADIN` (no spec gate); they are useful in both specs, no duplication.

Total 20 flat children. Only one spec's 9 icon slots load at a time, so the two
sets never overlap on screen. WeakAuras reloads on the spellknown condition when
you respec, switching sets automatically. All Ret uids preserved → wago treats it
as the same aura (new version via "Import new string").

**Spec discriminators:** Crusader Strike (35395) is the 20-pt Ret talent; Holy
Shield (20925) is a deep Prot talent. A deep Ret build won't know Holy Shield and
vice-versa, so the two gates are mutually exclusive in practice.

## Prot trigger logic (new TSU, modelled on the Ret trigger)

Reuses the shared helpers from the Ret trigger: `nameicon`, `cd` (ready/soon/
notyet by GetSpellCooldown, GCD-aware), `track`/`fresh` (pre-ready timing in
`aura_env`), `affordable` (mana gate by **spell name** = max rank, per v1.5.1),
the centering block, and `while #q>5 do q[#q]=nil end`.

Priority (insertion order into the queue = priority; leftmost rendered icon = press
now). Maintenance items jump to the front when missing; actives follow.

**Maintenance (front when missing):**
1. **Righteous Fury** (25780) — suggested when the player buff is not active
   (critical for tank threat; long duration so rarely drops mid-fight).
2. **Blessing of Sanctuary** — suggested when no blessing is up (recognise normal
   + Greater). No low-mana swap to Blessing of Wisdom (Prot keeps Sanctuary).
3. **Aura** — suggested when no Paladin aura is active (reuse `hasAura`); the
   suggested icon is **Devotion Aura** (tank default).
4. **Seal of Righteousness** — suggested when no seal is up. Low-mana awareness:
   mana <12% → soft hint **Seal of Wisdom**; back >40% → point back to the
   offensive seal (remember whichever offensive seal is used). Never blocks.

**Actives (cooldown-gated, ready/soon pre-ready sweep like Ret):**
5. **Holy Shield** (20925) — top active.
6. **Avenger's Shield** (31935) — raised above Consecration/Judgement per user.
7. **Consecration** — by name; **always** shown when off cd (NOT enemy-count
   gated, unlike Ret — it is core single-target threat for a tank).
8. **Judgement** (20271).
9. **Hammer of Wrath** (24274) — execute, target ≤20% HP.
10. **Exorcism** (879) — only vs Undead/Demon (`UnitCreatureType`).

**Shared with Ret:** mana-gate by name (v1.5.1), pre-ready sweep + sparkle, queue
cap to 5, auto-centering. **Disarm gate does NOT apply to Prot** — none of the
suggested Prot abilities is a weapon attack (all are spells), so disarm hides
nothing.

## Build / encoding approach

- Build FROM the canonical v1.5.1 string (`rexhail-rotation-ret.import.txt`) so the
  Ret slots and shared bars carry over verbatim.
- Add the `spellknown=35395` load gate to the 9 Ret slots (edit `load` only).
- Synthesise 9 Prot slots by cloning a Ret slot's region/visual fields (uid →
  `RexhailProt_sN`, load gate `spellknown=20925`) and swapping in the Prot TSU
  custom code, keeping `local j=N` per slot for centering.
- Bump `d.semver` to `2.0.0`. Optionally rename root `d.id` "…Ret Paladin" →
  "…Paladin" (cosmetic; wago listing title is set separately on the site).
- Encode via the canonical pipeline (LibSerialize → raw DEFLATE → EncodeForPrint).

## Verification

- Offline (lupa, stubbed WoW globals): for the Prot trigger, assert the queue
  builds the expected ordering across the 9 slots under representative states
  (no buffs → maintenance front-jumps; full maintenance → actives only; ≤20% HP
  → HoW appears; Undead target → Exorcism; low mana → Seal of Wisdom hint + spells
  you can't afford hidden). Re-run the Ret offline tests unchanged.
- Structural asserts: 20 children, uids = `RexhailRet_s1..s9` +
  `RexhailProt_s1..s9` + gcd + swing; Ret slots' trigger custom byte-identical to
  v1.5.1; Ret slots gated `spellknown=35395`, Prot slots `spellknown=20925`;
  visual fields (cooldown=true, inverse=true, customVariables, 3 subRegions incl.
  ACShine) present on Prot slots too.
- `demo_roundtrip.py` sanity on the final string.
- **In-game gate (CLAUDE.md §2):** do NOT commit/promote to canonical or publish
  to wago until Robert tests in Prot spec in WoW and confirms "działa".

## Out of scope (YAGNI)

- No prot-specific GCD/swing bars (shared bars suffice).
- No single-target/AoE toggle for Prot Consecration (always on).
- No nested groups, no dynamic group region.
- No automatic stance/aura switching — suggestions only.
