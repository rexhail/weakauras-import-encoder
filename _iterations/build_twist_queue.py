#!/usr/bin/env python3
"""
build_twist_queue.py — v3.9.6: seal timer + seal-based swing bar color

Na bazie v3.3.0 (canonical), aplikuje wszystkie patche SoV + opener + combat gate:
  P1  - twistSeal + SoV (31801) we wszystkich childrenach
  P2  - twistUp  + "Seal of Vengeance" w Tier B kolejce (c[1]-c[9])
  P3  - recentTwist + "Seal of Vengeance" w c[22]
  P4  - GetActiveStates fallback usuniety (crashuje w WA), tylko GetSwingTimerInfo
  P5  - JotC detection + opener block (SotC->Judge) + combat gate, SoV push REMOVED
  P6  - SoC return + zamkniecie combat gate (end) + B.queue=q
  P7  - c[21] seal indicator: TSU + trigger check=update (sync fix)
  P8  - c[1]-c[9] Judge: cs~="notyet" -> cs=="ready" (hide on CD)
  P9  - c[20] RexhailRet_swing: disabled=true + alpha=0 (replaced by c[22])
  P10 - c[22] przesuniecie na pozycje c[20] (yOffset)
  P11 - c[1] throttle 100ms: early return if called <100ms ago (CPU reduction)
  P12 - c[1] nameplates cache: 300ms TTL to avoid expensive per-frame scan
  P13 - Prot branch: Seal of Wisdom + cs==ready (was cs~=notyet)
  P15 - c[21] seal indicator: Prot-aware (shows SoW for Prot spec)
  P16 - c[22] swing timer: visible for Prot spec (was Ret Tier B only)
  P17 - c[22] swing bar: seal-based color (SoC=orange, SotC=gold, SoW=blue, ...)
  P18 - c[21] seal timer: subtext %p below icon (WA built-in token, ~1 decimal sec)
"""
import sys, os, tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import weakauras_encoder as wa

ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE  = os.path.join(ROOT, "rexhail-rotation-ret.import.txt")
OUT   = os.path.join(ROOT, "_iterations", "rexhail-rotation-ret-v3.9.6.import.txt")

NEW_VERSION = "3.9.6"

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

# P11: throttle c[1] main brain — skip if called <100ms ago
P11_THROTTLE_OLD = 'function(allstates)\n\n  local S = aura_env\n'
P11_THROTTLE_NEW = 'function(allstates)\n\n  local S = aura_env\n  local now=GetTime(); if S._lastRun and now-S._lastRun<0.1 then return false end; S._lastRun=now\n'

# P12: cache nameplates scan result for 300ms (expensive per-mob loop)
P12_NPCACHE_OLD = \
"""local function enemies()
    local c=0
    if C_NamePlate and C_NamePlate.GetNamePlates then
      for _,p in ipairs(C_NamePlate.GetNamePlates()) do
        local u=p.namePlateUnitToken
        if u and UnitCanAttack("player",u) and not UnitIsDead(u)
           and (IsSpellInRange("Judgement",u)==1 or IsSpellInRange("Crusader Strike",u)==1) then c=c+1 end
      end
    end
    return c
  end"""

P12_NPCACHE_NEW = \
"""local function enemies()
    local now=GetTime()
    if S._npCache and now-S._npCache.t<0.3 then return S._npCache.n end
    local c=0
    if C_NamePlate and C_NamePlate.GetNamePlates then
      for _,p in ipairs(C_NamePlate.GetNamePlates()) do
        local u=p.namePlateUnitToken
        if u and UnitCanAttack("player",u) and not UnitIsDead(u)
           and (IsSpellInRange("Judgement",u)==1 or IsSpellInRange("Crusader Strike",u)==1) then c=c+1 end
      end
    end
    S._npCache={t=now,n=c}
    return c
  end"""

# P13: Prot branch rewrite — adds Seal of Wisdom + fixes cs~="notyet" -> cs=="ready"
P13_PROT_OLD = \
'if B.spec=="prot" then\n    local q={}\n    local hasRF=false\n    for i=1,40 do local nm=UnitBuff("player",i); if not nm then break end\n      if nm:find("Righteous Fury") then hasRF=true; break end end\n    if not hasRF then local n,ic=nameicon(25780); push(q,n or "Righteous Fury",ic,25780,"ready",0) end\n    if not curBless and known(20914) then local n,ic=nameicon(20914); push(q,n,ic,20914,"ready",0) end\n    if not hasAura() then local n,ic=nameicon(465); push(q,n,ic,465,"ready",0) end\n    if known(20925) then local n,ic=nameicon(20925); local cs,rm=cd(n,20925); track(20925,cs)\n      if cs~="notyet" and affordable(20925) then push(q,n,ic,20925,cs,rm) end end\n    if known(31935) then local n,ic=nameicon(31935); local cs,rm=cd(n,31935); track(31935,cs)\n      if cs~="notyet" and affordable(31935) then push(q,n,ic,31935,cs,rm) end end\n    if known(26573) then local _,_,cic=GetSpellInfo("Consecration"); local cs,rm=cd("Consecration",26573); track(26573,cs)\n      if cs~="notyet" and affordable("Consecration") then push(q,"Consecration",cic,"Consecration",cs,rm) end end\n    do local n,ic=nameicon(20271); local cs,rm=cd(n,20271); track(20271,cs)\n      if cs~="notyet" and affordable(20271) then push(q,n,ic,20271,cs,rm) end end\n    do local n,ic=nameicon(24274); local cs,rm=cd(n,24274); track(24274,cs)\n      if tEx and hp<=0.2 and cs~="notyet" and affordable(24274) then push(q,n,ic,24274,cs,rm) end end\n    do local n,ic=nameicon(879); local ct=tEx and UnitCreatureType("target"); local cs,rm=cd(n,879); track(879,cs)\n      if tEx and (ct=="Undead" or ct=="Demon") and cs~="notyet" and affordable(879) then push(q,n,ic,879,cs,rm) end end\n    B.queue=q\n  end'

P13_PROT_NEW = \
'if B.spec=="prot" then\n    local q={}\n    local hasRF=false\n    for i=1,40 do local nm=UnitBuff("player",i); if not nm then break end\n      if nm:find("Righteous Fury") then hasRF=true; break end end\n    if not hasRF then local n,ic=nameicon(25780); push(q,n or "Righteous Fury",ic,25780,"ready",0) end\n    if not curSeal then\n      local _n,_,_ic=GetSpellInfo("Seal of Wisdom"); if _n then push(q,_n,_ic,"Seal of Wisdom","ready",0) end\n    end\n    if known(20925) then local n,ic=nameicon(20925); local cs,rm=cd(n,20925); track(20925,cs)\n      if cs=="ready" and affordable(20925) then push(q,n,ic,20925,cs,rm) end end\n    if known(26573) then local _,_,cic=GetSpellInfo("Consecration"); local cs,rm=cd("Consecration",26573); track(26573,cs)\n      if cs=="ready" and affordable("Consecration") then push(q,"Consecration",cic,"Consecration",cs,rm) end end\n    if not curBless and known(20914) then local n,ic=nameicon(20914); push(q,n,ic,20914,"ready",0) end\n    if not hasAura() then local n,ic=nameicon(465); push(q,n,ic,465,"ready",0) end\n    if known(31935) then local n,ic=nameicon(31935); local cs,rm=cd(n,31935); track(31935,cs)\n      if cs=="ready" and affordable(31935) then push(q,n,ic,31935,cs,rm) end end\n    do local n,ic=nameicon(20271); local cs,rm=cd(n,20271); track(20271,cs)\n      if cs=="ready" and affordable(20271) then push(q,n,ic,20271,cs,rm) end end\n    do local n,ic=nameicon(24274); local cs,rm=cd(n,24274); track(24274,cs)\n      if tEx and hp<=0.2 and cs=="ready" and affordable(24274) then push(q,n,ic,24274,cs,rm) end end\n    do local n,ic=nameicon(879); local ct=tEx and UnitCreatureType("target"); local cs,rm=cd(n,879); track(879,cs)\n      if tEx and (ct=="Undead" or ct=="Demon") and cs=="ready" and affordable(879) then push(q,n,ic,879,cs,rm) end end\n    B.queue=q\n  end'

# P16: c[22] swing timer visible for Prot spec
P16_SWING_OLD = '    B.twist={state=st, swingRem=rem, combo=S.combo, duration=dur, expiry=exp}\n  end\n\n  local b=B.twist'
P16_SWING_NEW = '    B.twist={state=st, swingRem=rem, combo=S.combo, duration=dur, expiry=exp}\n  elseif B.spec=="prot" then\n    local rem, dur, exp\n    if WeakAuras and WeakAuras.GetSwingTimerInfo then\n      dur, exp = WeakAuras.GetSwingTimerInfo("main")\n      if exp and exp>0 then rem = exp - GetTime() end\n    end\n    if dur and exp then B.twist={state="idle",swingRem=rem,combo=0,duration=dur,expiry=exp} end\n  end\n\n  local b=B.twist'

# P17: c[22] swing bar color per active seal (via WA conditions, not TSU)
# Just expose st.seal so WA conditions engine can check it
P17_SEALCOLOR_OLD = '    allstates[""]=st\n  elseif allstates[""]'
P17_SEALCOLOR_NEW = (
    '    st.seal=curSeal or ""\n'
    '    allstates[""]=st\n  elseif allstates[""]'
)


# P7 (c[21] seal indicator): show recommended seal when no seal active
# - opener mode (target, no JotC): show SotC
# - combat/no target:              show SoC
# icon is desaturated + red border stays (noseal=true) to show "not active yet"
SEAL_IND_TSU = '''\
function(allstates)
  local S = aura_env
  local sName, sIcon, sDur, sExp
  for i=1,40 do
    local nm, ic, _, _, dur, exp = UnitBuff("player", i)
    if not nm then break end
    if nm:find("^Seal of ") then sName, sIcon, sDur, sExp = nm, ic, dur or 0, exp or 0; break end
  end
  local st = allstates[""] or {}
  st.show, st.changed = true, true
  if sName then
    if sName~="Seal of Wisdom" and sName~="Seal of Light" then S.lastSealIcon, S.lastSealName = sIcon, sName end
    st.icon, st.name = sIcon, sName
    st.noseal, st.desaturate = false, false
    st.progressType = "timed"
    st.duration = sDur
    st.expirationTime = sExp
  else
    local tEx = UnitExists("target") and UnitCanAttack("player","target") and not UnitIsDead("target")
    local jotc = false
    if tEx then for i=1,40 do local dn=UnitDebuff("target",i); if not dn then break end
      if dn=="Judgement of the Crusader" then jotc=true; break end end end
    local isProt = IsSpellKnown(20925) or IsPlayerSpell(20925)
    local suggSeal = isProt and "Seal of Wisdom" or (tEx and not jotc and "Seal of the Crusader" or "Seal of Command")
    local rn,_,ri = GetSpellInfo(suggSeal)
    st.icon = ri or S.lastSealIcon or select(3, GetSpellInfo(21084))
    st.name = rn or S.lastSealName or "No Seal"
    st.noseal, st.desaturate = true, true
    st.progressType = "none"
    st.duration = 0
    st.expirationTime = 0
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

# P13: Prot branch rewrite (SoW + cs==ready) — MUST be before P8 which also patches Prot Judge!
# Apply to all c[1]-c[9] since they all have the Prot branch
for idx in range(1, 10):
    code = get_tsu(lua, idx)
    if P13_PROT_OLD in code:
        code = apply(code, P13_PROT_OLD, P13_PROT_NEW, f"P13 c[{idx}]")
        set_tsu(lua, g, idx, code)
        changed.append(f"c[{idx}]:P13-prot-sow-csready")

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

# P18: seal timer on c[21]
# %p = only working approach (WA built-in token, rendered by WA's own text engine).
# cooldownTextDisabled=false doesn't work in TBC — no native cooldown numbers in WoW TBC.
# %p always shows one decimal; no WA config option overrides this in this version.
lua.execute(r'''
table.insert(tbl.c[21].subRegions, {
    type = "subtext",
    anchor_point = "INNER_BOTTOM",
    anchorXOffset = 0,
    anchorYOffset = -10,
    rotateText = "NONE",
    text_automaticWidth = "Auto",
    text_color = {1, 1, 1, 1},
    text_fixedWidth = 64,
    text_font = "Friz Quadrata TT",
    text_fontSize = 12,
    text_fontType = "OUTLINE",
    text_text = "%p",
    text_justify = "CENTER",
    text_wordWrap = true,
    text_visible = true
})
''')
changed.append("c[21]:P18-seal-timer-subtext")

# P9: hide old swing timer (c[20] RexhailRet_swing) — disabled=true failed in-game, use alpha=0
lua.execute("tbl.c[20].disabled = true")
lua.execute("tbl.c[20].alpha = 0")
changed.append("c[20]:P9-disableOldSwing")
# P10: move c[22] (color-changing swing) to c[20]'s y position (bottom slot)
lua.execute("tbl.c[22].yOffset = tbl.c[20].yOffset")
changed.append("c[22]:P10-reposition")

# P11: throttle
c1_code = get_tsu(lua, 1)
c1_code = apply(c1_code, P11_THROTTLE_OLD, P11_THROTTLE_NEW, "P11")
set_tsu(lua, g, 1, c1_code)
changed.append("c[1]:P11-throttle-100ms")

# P12: nameplates cache
c1_code = get_tsu(lua, 1)
c1_code = apply(c1_code, P12_NPCACHE_OLD, P12_NPCACHE_NEW, "P12")
set_tsu(lua, g, 1, c1_code)
changed.append("c[1]:P12-npcache-300ms")

# P16: Prot swing timer in c[22]
c22_code = get_tsu(lua, 22)
c22_code = apply(c22_code, P16_SWING_OLD, P16_SWING_NEW, "P16")
# P17: seal-based bar color in c[22]
c22_code = apply(c22_code, P17_SEALCOLOR_OLD, P17_SEALCOLOR_NEW, "P17")
set_tsu(lua, g, 22, c22_code)
changed.append("c[22]:P16-prot-swingtimer")
changed.append("c[22]:P17-seal-color")

# P17d: declare 'seal' in c[22] customVariables so WA Conditions can check it
lua.execute("tbl.c[22].triggers[1].trigger.customVariables = '{twiststate = \"string\", combo = \"string\", seal = \"string\"}'")
changed.append("c[22]:P17d-seal-customvariable")

# P17c: insert seal-based barColor conditions before existing twist-state conditions
lua.execute(r'''
local newConds = {
    {check={trigger=1,op="==",variable="seal",value=""},         changes={{property="barColor",value={0.8,0.15,0.15,1}}}},
    {check={trigger=1,op="==",variable="seal",value="Seal of Command"},         changes={{property="barColor",value={1,0.55,0,1}}}},
    {check={trigger=1,op="==",variable="seal",value="Seal of the Crusader"},    changes={{property="barColor",value={1,0.85,0.1,1}}}},
    {check={trigger=1,op="==",variable="seal",value="Seal of Wisdom"},          changes={{property="barColor",value={0.3,0.65,1,1}}}},
    {check={trigger=1,op="==",variable="seal",value="Seal of Righteousness"},   changes={{property="barColor",value={0.8,0.8,1,1}}}},
    {check={trigger=1,op="==",variable="seal",value="Seal of Blood"},           changes={{property="barColor",value={1,0.13,0.13,1}}}},
    {check={trigger=1,op="==",variable="seal",value="Seal of the Martyr"},      changes={{property="barColor",value={1,0.13,0.13,1}}}},
    {check={trigger=1,op="==",variable="seal",value="Seal of Vengeance"},       changes={{property="barColor",value={0.5,0.25,1,1}}}},
}
for i = #newConds, 1, -1 do
    table.insert(tbl.c[22].conditions, 1, newConds[i])
end
''')
changed.append("c[22]:P17c-seal-conditions")



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
assert 'B.spec=="prot"' in c22,                 "P16 missing: Prot branch not in c[22] TSU"
assert 'st.seal=curSeal' in c22,                "P17 missing: st.seal not set in c[22] TSU"

c22_final = get_tsu(lua, 22)
cond_count = int(lua.eval('#tbl.c[22].conditions'))
assert cond_count >= 10, f"P17c: expected 10 conditions on c[22], got {cond_count}"

c22_cond1_var = str(lua.eval('tbl.c[22].conditions[1].check.variable'))
assert c22_cond1_var == 'seal', f"P17c: first condition must check 'seal', got {c22_cond1_var}"

c22_cond_last = str(lua.eval('tbl.c[22].conditions[' + str(int(lua.eval('#tbl.c[22].conditions'))) + '].check.variable'))
assert c22_cond_last == 'twiststate', f"P17c: last condition must be twiststate (window/success), got {c22_cond_last}"

# P17d verify: seal in customVariables
cv = str(lua.eval('tbl.c[22].triggers[1].trigger.customVariables'))
assert 'seal' in cv, "P17d missing: 'seal' not in c[22] customVariables"

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

assert 'Seal of Wisdom' in c1,           "P13 missing: Seal of Wisdom not in Prot branch"
# Check that Prot section has cs=="ready" for its spells
prot_start = c1.find('if B.spec=="prot"')
prot_end = c1.find('B.queue=q', prot_start) + len('B.queue=q')
next_end = c1.find('end', prot_end)
prot_section = c1[prot_start:next_end+3]
assert 'cs=="ready"' in prot_section,    "P13 missing: cs==ready gate not in Prot branch"
assert 'cs~="notyet"' not in prot_section, "P13 regression: cs~=notyet still present in Prot section"

assert t2['c'][20]['disabled'] == True,                                "P9 missing (c[20] not disabled)"
assert t2['c'][20]['alpha'] == 0,                                      "P9 missing (c[20] alpha not 0)"
assert t2['c'][22]['yOffset'] == t2['c'][20]['yOffset'],               "P10 missing (c[22] yOffset not moved to c[20] position)"
assert 'S._lastRun' in c1,        "P11 missing: throttle sentinel not in c[1] TSU"
assert 'now-S._lastRun<0.1' in c1, "P11 missing: throttle interval not in c[1] TSU"
assert 'S._npCache' in c1,         "P12 missing: nameplates cache variable not in c[1] TSU"
assert '_npCache.t<0.3' in c1,     "P12 missing: nameplates cache TTL check not in c[1] TSU"

# P18 verify assertions
c21_tsu = get_tsu(lua, 21)
assert 'st.progressType = "timed"' in c21_tsu or 'st.progressType="timed"' in c21_tsu, "P18: progressType not set in c[21] TSU"
assert 'st.expirationTime' in c21_tsu, "P18: expirationTime not set in c[21] TSU"
assert 'st.duration' in c21_tsu, "P18: duration not set in c[21] TSU"
sr_count = int(lua.eval('#tbl.c[21].subRegions'))
found_p = any(
    str(lua.eval(f'tbl.c[21].subRegions[{i}].type')) == "subtext" and
    str(lua.eval(f'tbl.c[21].subRegions[{i}].text_text')) == "%p"
    for i in range(1, sr_count + 1)
)
assert found_p, "P18: No subtext with '%p' token found in c[21].subRegions"

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
