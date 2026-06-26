#!/usr/bin/env python3
"""
build_twist_queue.py — v3.9.2: Judge no-grey (Tier B fix) + swing timer reposition

Na bazie v3.3.0 (canonical), aplikuje wszystkie patche SoV + opener + combat gate:
  P1 - twistSeal + SoV (31801) we wszystkich childrenach
  P2 - twistUp  + "Seal of Vengeance" w Tier B kolejce (c[1]-c[9])
  P3 - recentTwist + "Seal of Vengeance" w c[22]
  P4 - GetActiveStates fallback usuniety (crashuje w WA), tylko GetSwingTimerInfo
  P5 - JotC detection + opener block (SotC->Judge) + combat gate, SoV push REMOVED
  P6 - SoC return + zamkniecie combat gate (end) + B.queue=q
  P7 - c[21] seal indicator: TSU + trigger check=update (sync fix)
  P8 - c[1]-c[9] Judge: cs~="notyet" -> cs=="ready" (hide on CD)
  P9 - c[20] RexhailRet_swing: disabled=true (replaced by c[22])
"""
import sys, os, tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import weakauras_encoder as wa

ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE  = os.path.join(ROOT, "rexhail-rotation-ret.import.txt")
OUT   = os.path.join(ROOT, "_iterations", "rexhail-rotation-ret-v3.9.2.import.txt")

NEW_VERSION = "3.9.2"

# -- patches -------------------------------------------------------------------

# P1: twistSeal detection - dodaje SoV 31801
P1_OLD = '(known(31892) and 31892) or (known(348700) and 348700) or nil'
P1_NEW = '(known(31892) and 31892) or (known(348700) and 348700) or (known(31801) and 31801) or nil'

# P2: twistUp buff scan - dodaje "Seal of Vengeance"
P2_OLD = 'if nm=="Seal of Blood" or nm=="Seal of the Martyr" then twistUp=true; break end end'
P2_NEW = 'if nm=="Seal of Blood" or nm=="Seal of the Martyr" or nm=="Seal of Vengeance" then twistUp=true; break end end'

# P3: recentTwist names w c[22]
P3_OLD = '(S.lastCast=="Seal of Blood" or S.lastCast=="Seal of the Martyr")'
P3_NEW = '(S.lastCast=="Seal of Blood" or S.lastCast=="Seal of the Martyr" or S.lastCast=="Seal of Vengeance")'

# P4: GetActiveStates fallback w c[22] - noop (GetActiveStates crashuje, pozostawiamy GetSwingTimerInfo)
P4_OLD = '''\
    local rem, dur, exp
    if WeakAuras and WeakAuras.GetSwingTimerInfo then
      dur, exp = WeakAuras.GetSwingTimerInfo("main")
      if exp and exp>0 then rem = exp - GetTime() end
    end'''
P4_NEW = '''\
    local rem, dur, exp
    if WeakAuras and WeakAuras.GetSwingTimerInfo then
      dur, exp = WeakAuras.GetSwingTimerInfo("main")
      if exp and exp>0 then rem = exp - GetTime() end
    end'''

# P5: JotC opener gate + swing data + seal push
#     Zastepuje caly blok swing+seal z v3.5.x nowa logika z openerem
#     Stosowany PO P2 (szuka zaktualizowanego stringa z SoV)
P5_OLD = '''\
      if nm=="Seal of Blood" or nm=="Seal of the Martyr" or nm=="Seal of Vengeance" then twistUp=true; break end end
    local blessId'''
P5_NEW = '''\
      if nm=="Seal of Blood" or nm=="Seal of the Martyr" or nm=="Seal of Vengeance" then twistUp=true; break end end
    -- JotC debuff detection (Judgement of the Crusader = applied via Judge with SotC active)
    local jotc=false
    if tEx then for i=1,40 do local dn=UnitDebuff("target",i); if not dn then break end
      if dn=="Judgement of the Crusader" then jotc=true; break end end end
    -- swing data
    local swingRem
    if WeakAuras and WeakAuras.GetSwingTimerInfo then
      local _,swe=WeakAuras.GetSwingTimerInfo("main")
      if swe and swe>GetTime() then swingRem=swe-GetTime() end
    end
    local PAYOFF_ID=(known(31892) and 31892) or (known(348700) and 348700) or (known(31801) and 31801)
    local PRIMARY_ID=20375
    -- OPENER: no JotC on target -> suggest SotC then Judge
    if tEx and not jotc then
      if curSeal~="Seal of the Crusader" then
        local sn,_,si=GetSpellInfo("Seal of the Crusader")
        if sn then push(q,sn,si,sn,"ready",0) end
      else
        local n,ic=nameicon(20271); local cs,rm=cd(n,20271)
        if cs=="ready" and affordable(20271) then push(q,n,ic,20271,cs,rm) end
      end
    end
    -- COMBAT GATE: rotation only when JotC active OR no target
    if jotc or not tEx then
    if not curSeal then
      local n,ic=nameicon(PRIMARY_ID)
      if affordable(PRIMARY_ID) then push(q,n,ic,PRIMARY_ID,"ready",0) end
    end
    local blessId'''

# P6: SoC return + zamkniecie combat gate, przed B.queue=q
P6_OLD = '''\
    do local n,ic=nameicon(879); local ct=tEx and UnitCreatureType("target"); local cs,rm=cd(n,879); track(879,cs)
      if tEx and (ct=="Undead" or ct=="Demon") and cs~="notyet" and affordable(879) then push(q,n,ic,879,cs,rm) end end
    B.queue=q
  end

  if B.spec=="prot" then'''
P6_NEW = '''\
    do local n,ic=nameicon(879); local ct=tEx and UnitCreatureType("target"); local cs,rm=cd(n,879); track(879,cs)
      if tEx and (ct=="Undead" or ct=="Demon") and cs~="notyet" and affordable(879) then push(q,n,ic,879,cs,rm) end end
    -- return to SoC when in payoff seal and CS/Judge on CD (rearm for next twist)
    if twistUp and PRIMARY_ID then
      local n,ic=nameicon(PRIMARY_ID); push(q,n,ic,PRIMARY_ID,"ready",0)
    end
    end -- jotc gate
    B.queue=q
  end

  if B.spec=="prot" then'''

# P8: Judge only when cs=="ready", no grey flag (seal indicator handles seal state messaging)
# Three patterns for Ret and Prot variants
P8_RET_OLD = 'if cs~="notyet" and affordable(20271) then push(q,n,ic,20271,cs,rm, not curSeal) end end'
P8_RET_NEW = 'if cs=="ready" and affordable(20271) then push(q,n,ic,20271,cs,rm) end end'
P8_PROT1_OLD = 'if cs~="notyet" and affordable(20271) then push(q,n,ic,20271,cs,rm, not twistUp) end end'
P8_PROT1_NEW = 'if cs=="ready" and affordable(20271) then push(q,n,ic,20271,cs,rm) end end'
P8_PROT2_OLD = 'if cs~="notyet" and affordable(20271) then push(q,n,ic,20271,cs,rm) end end\n    do local n,ic=nameicon(24274)'
P8_PROT2_NEW = 'if cs=="ready" and affordable(20271) then push(q,n,ic,20271,cs,rm) end end\n    do local n,ic=nameicon(24274)'

# P7 (c[21] seal indicator): show recommended seal when no seal active
# - opener mode (target, no JotC): show SotC
# - combat/no target:              show SoC
# icon is desaturated + red border stays (noseal=true) to show "not active yet"
SEAL_IND_TSU = '''\
function(allstates)
  local S = aura_env
  local sName, sIcon
  for i=1,40 do
    local nm, ic = UnitBuff("player", i)
    if not nm then break end
    if nm:find("^Seal of ") then sName, sIcon = nm, ic; break end
  end
  local st = allstates[""] or {}
  st.show, st.changed = true, true
  if sName then
    if sName~="Seal of Wisdom" and sName~="Seal of Light" then S.lastSealIcon, S.lastSealName = sIcon, sName end
    st.icon, st.name = sIcon, sName
    st.noseal, st.desaturate = false, false
  else
    local tEx = UnitExists("target") and UnitCanAttack("player","target") and not UnitIsDead("target")
    local jotc = false
    if tEx then for i=1,40 do local dn=UnitDebuff("target",i); if not dn then break end
      if dn=="Judgement of the Crusader" then jotc=true; break end end end
    local rn,_,ri = GetSpellInfo(tEx and not jotc and "Seal of the Crusader" or "Seal of Command")
    st.icon = ri or S.lastSealIcon or select(3, GetSpellInfo(21084))
    st.name = rn or S.lastSealName or "No Seal"
    st.noseal, st.desaturate = true, true
  end
  allstates[""] = st
  return true
end'''

# -- helpers -------------------------------------------------------------------

def get_tsu(lua, idx):
    lua.execute(f"_ci = tbl.c[{idx}]")
    return str(lua.eval("_ci.triggers[1].trigger.custom or ''"))

def set_tsu(lua, g, idx, code):
    g._new_tsu = code
    lua.execute(f"tbl.c[{idx}].triggers[1].trigger.custom = _new_tsu")

def apply(code, old, new, label):
    if old not in code:
        raise ValueError(f"Patch '{label}' not found in c[?] TSU")
    return code.replace(old, new)

# -- build ---------------------------------------------------------------------

raw = open(BASE).read().strip()
blob = wa.decode(raw)
lua, LS = wa._lua()
g = lua.globals()
g.LS = LS; g.data = blob
lua.execute("ok,tbl = LS:Deserialize(data); assert(ok,'deser')")

base_ver = str(lua.eval("tbl.d.semver"))
assert base_ver == "3.3.0", f"Expected base 3.3.0, got {base_ver}"
print(f"[build] base: {base_ver}  ->  {NEW_VERSION}")

n_children = 0
while True:
    lua.execute(f"_ok = tbl.c[{n_children+1}] ~= nil")
    if not lua.eval("_ok"): break
    n_children += 1

changed = []

# P1: twistSeal - wszystkie children ktore maja ten kod
for idx in range(1, n_children + 1):
    code = get_tsu(lua, idx)
    if P1_OLD in code:
        set_tsu(lua, g, idx, code.replace(P1_OLD, P1_NEW))
        changed.append(f"c[{idx}]:P1")

# P2: twistUp - c[1]-c[9]
for idx in range(1, 10):
    code = get_tsu(lua, idx)
    if P2_OLD in code:
        set_tsu(lua, g, idx, code.replace(P2_OLD, P2_NEW))
        changed.append(f"c[{idx}]:P2")

# P3+P4: c[22] only
code22 = get_tsu(lua, 22)
code22 = apply(code22, P3_OLD, P3_NEW, "P3-recentTwist")
code22 = apply(code22, P4_OLD, P4_NEW, "P4-GetActiveStates")
set_tsu(lua, g, 22, code22)
changed.append("c[22]:P3"); changed.append("c[22]:P4")

# P5: JotC gate + opener - c[1]-c[9] (po P2, szuka zaktualizowanego SoV stringa)
for idx in range(1, 10):
    code = get_tsu(lua, idx)
    code = apply(code, P5_OLD, P5_NEW, f"P5-openerGate c[{idx}]")
    set_tsu(lua, g, idx, code)
    changed.append(f"c[{idx}]:P5")

# P6: SoC return + zamkniecie gate - c[1]-c[9]
for idx in range(1, 10):
    code = get_tsu(lua, idx)
    code = apply(code, P6_OLD, P6_NEW, f"P6-closeGate c[{idx}]")
    set_tsu(lua, g, idx, code)
    changed.append(f"c[{idx}]:P6")

# P8: Judge only when ready - c[1]-c[9] (Ret and Prot variants)
for idx in range(1, 10):
    code = get_tsu(lua, idx)
    code = apply(code, P8_RET_OLD, P8_RET_NEW, f"P8-judgeReady-Ret c[{idx}]")
    # Prot variants may not exist in all slots
    if P8_PROT1_OLD in code:
        code = code.replace(P8_PROT1_OLD, P8_PROT1_NEW)
    if P8_PROT2_OLD in code:
        code = code.replace(P8_PROT2_OLD, P8_PROT2_NEW)
    set_tsu(lua, g, idx, code)
    changed.append(f"c[{idx}]:P8")

# P7: seal indicator - show recommended seal + fix trigger to run every frame
set_tsu(lua, g, 21, SEAL_IND_TSU)
lua.execute("tbl.c[21].triggers[1].trigger.check = 'update'")
lua.execute("tbl.c[21].triggers[1].trigger.events = nil")
changed.append("c[21]:P7-sealIndicator")
changed.append("c[21]:P7-triggerUpdate")

# P9: hide old swing timer (c[20] RexhailRet_swing) — disabled=true failed in-game, use alpha=0
lua.execute("tbl.c[20].disabled = true")
lua.execute("tbl.c[20].alpha = 0")
changed.append("c[20]:P9-disableOldSwing")
# P10: move c[22] (color-changing swing) to c[20]'s y position (bottom slot)
lua.execute("tbl.c[22].yOffset = tbl.c[20].yOffset")
changed.append("c[22]:P10-reposition")

print(f"[build] patches: {len(changed)}")

# version + desc
g._new_ver = NEW_VERSION
lua.execute("tbl.d.semver = _new_ver")
desc = str(lua.eval("tbl.d.desc or ''"))
if "v3.3.0" in desc: desc = desc.replace("v3.3.0", f"v{NEW_VERSION}")
elif f"v{NEW_VERSION}" not in desc: desc = f"v{NEW_VERSION} -- " + desc
g._new_desc = desc
lua.execute("tbl.d.desc = _new_desc")

# serialize
fd, tmp = tempfile.mkstemp(suffix=".ser"); os.close(fd)
g._tmp = tmp.replace("\\", "/")
lua.execute("local s=LS:Serialize(tbl); local f=io.open(_tmp,'wb'); f:write(s); f:close()")
modified = open(tmp, "rb").read(); os.remove(tmp)
final_str = wa.encode(modified)
open(OUT, "w").write(final_str)
print(f"[build] output  -> {os.path.basename(OUT)} ({len(final_str)} chars)")

# -- verify -------------------------------------------------------------------

ok2, t2 = wa.deserialize(wa.decode(final_str))
assert ok2
assert str(t2['d']['semver']) == NEW_VERSION

c1 = str(t2['c'][1]['triggers'][1]['trigger']['custom'])
c22 = str(t2['c'][22]['triggers'][1]['trigger']['custom'])
assert "known(31801)" in c1,                    "P1 missing"
assert "Seal of Vengeance" in c1,               "P2 missing"
assert "jotc" in c1,                            "P5 missing (jotc)"
assert "Judgement of the Crusader" in c1,       "P5 missing (JotC debuff)"
assert "Seal of the Crusader" in c1,            "P5 missing (SotC opener)"
assert "jotc or not tEx" in c1,                 "P5 missing (combat gate)"
assert "end -- jotc gate" in c1,                "P6 missing (gate close)"
assert "Seal of Vengeance" in c22,              "P3 missing"
assert "GetSwingTimerInfo" in c22,              "P4 GetSwingTimerInfo missing"

c21 = str(t2['c'][21]['triggers'][1]['trigger']['custom'])
assert "Judgement of the Crusader" in c21,      "P7 missing (jotc in seal indicator)"
assert "Seal of the Crusader" in c21,           "P7 missing (SotC in seal indicator)"
assert "Seal of Command" in c21,                "P7 missing (SoC in seal indicator)"
assert str(t2['c'][21]['triggers'][1]['trigger']['check']) == 'update', \
    "P7 missing (c[21] trigger check != update — indicator won't re-eval on target change)"

assert "swingRem<=0.4 and PAYOFF_ID" not in c1,                      "P5 regression (SoV push still present in queue)"
assert 'cs=="ready" and affordable(20271)' in c1,                      "P8 missing (Judge not gated on cs==ready)"
assert 'cs~="notyet" and affordable(20271)' not in c1,                 "P8 regression (old Judge condition still present)"
assert 'not curSeal) end end' not in c1,                               "P8 regression (Judge Tier A still has not curSeal grey flag)"
assert 'not twistUp) end end' not in c1,                               "P8 regression (Judge Tier B still has not twistUp grey flag)"
assert t2['c'][20]['disabled'] == True,                                "P9 missing (c[20] not disabled)"
assert t2['c'][20]['alpha'] == 0,                                      "P9 missing (c[20] alpha not 0)"
assert t2['c'][22]['yOffset'] == t2['c'][20]['yOffset'],               "P10 missing (c[22] yOffset not moved to c[20] position)"

# Lua syntax check (osobny runtime, bez stanu build)
lua2, _ = wa._lua()
g2 = lua2.globals()
for idx in [1, 21, 22]:
    tsu = str(t2['c'][idx]['triggers'][1]['trigger']['custom'])
    g2._chk = tsu
    err = lua2.eval("select(2, load('return '.._chk))")
    assert lua2.eval("load('return '.._chk) ~= nil"), f"c[{idx}] TSU syntax error: {err}"
    print(f"  c[{idx}] TSU kompiluje OK ({len(tsu)} chars)")

print(f"\n[build] verify OK -- {NEW_VERSION}, wszystkie patche potwierdzone")
print()
print(f"IMPORT: _iterations/rexhail-rotation-ret-v{NEW_VERSION}.import.txt")
print()
print(f"Flow w grze (v{NEW_VERSION}):")
print("  Bez celu            -> pelna rotacja (SoC/CS/Judge gotowe)")
print("  Cel bez JotC debuff -> OPENER: sugeruje SotC (jesli brak) lub Judge (jesli SotC aktywny)")
print("  Cel z JotC debuff   -> pelna rotacja: SoC (jesli brak), CS, Judge (tylko gdy ready)")
print("  Swing timer kolor   -> sygnal twistowania (SoV usuniety z kolejki rotacji)")
print("  SoV aktywny         -> ikona SoC na koncu kolejki (rearm)")

# -- behavior tests -----------------------------------------------------------
import subprocess, sys as _sys
_test = os.path.join(ROOT, "_iterations", "test_queue_behavior.py")
_r = subprocess.run([_sys.executable, _test], cwd=ROOT)
if _r.returncode != 0:
    raise SystemExit("[build] FAIL: behavior tests nie przeszly — nie importuj tego stringa")
