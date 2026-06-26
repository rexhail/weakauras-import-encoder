#!/usr/bin/env python3
"""
test_queue_behavior.py — sprawdza co rotacja faktycznie wyswietla dla kluczowych stanow gry.
Uzywa allstates[""] (output TSU), nie probuje czytac wewnetrznej kolejki (B.queue jest lokalne).

Centering layout: c[3] wyswietla slot 1 (najwyzszy priorytet), c[5] slot 2, c[7] slot 3.
Sprawdzamy te 3 sloty.

Uruchom: python3 _iterations/test_queue_behavior.py
"""
import sys, os, glob
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import weakauras_encoder as wa

# --- wczytaj najnowszy built import ---
files = sorted(glob.glob(os.path.join(os.path.dirname(__file__), 'rexhail-rotation-ret-v*.import.txt')))
assert files, "Brak pliku importu w _iterations/"
latest = files[-1]
print(f"Testuje: {os.path.basename(latest)}\n")

ok, tbl = wa.deserialize(wa.decode(open(latest).read().strip()))
assert ok, "Deserializacja nie powiodla sie"

# c[3] → slot 1 (queue[1]), c[5] → slot 2 (queue[2]), c[7] → slot 3 (queue[3])
DISPLAY_SLOTS = [3, 5, 7]
TSU = {i: str(tbl['c'][i]['triggers'][1]['trigger']['custom']) for i in DISPLAY_SLOTS}

# ---------------------------------------------------------------------------
BASE_STUBS = """
GetTime          = function() return 1000 end
UnitExists       = function(u) return u=="target" end
UnitCanAttack    = function() return true end
UnitIsDead       = function() return false end
UnitHealth       = function() return 50000 end
UnitHealthMax    = function() return 100000 end
UnitPower        = function() return 8000 end
UnitPowerMax     = function() return 10000 end
UnitCreatureType = function() return "Humanoid" end
IsSpellInRange   = function() return 1 end
GetInstanceInfo  = function() return "","none","","","none",0,0,0,0 end
C_NamePlate      = {GetNamePlates=function() return {} end}
WeakAuras        = {GetSwingTimerInfo=function() return 2.0, 1001.5 end}

local _sn = {
  [35395]="Crusader Strike",[20271]="Judgement",[26573]="Consecration",
  [20375]="Seal of Command",[21084]="Seal of Righteousness",
  [20218]="Retribution Aura",[465]="Devotion Aura",
  [19742]="Blessing of Wisdom",[19740]="Blessing of Might",
  [24274]="Hammer of Wrath",[879]="Exorcism",
  [31892]="Seal of Blood",[348700]="Seal of the Martyr",[31801]="Seal of Vengeance",
}
GetSpellInfo = function(id)
  local n = type(id)=="string" and id or (_sn[id] or tostring(id))
  return n, "", "Icon/"..n, 0, 0, 0, id
end

IsSpellKnown = function(id)
  return ({[35395]=true,[20375]=true,[20271]=true,[26573]=true,
           [20218]=true,[19740]=true,[31801]=true})[id] or false
end
IsPlayerSpell  = IsSpellKnown
IsUsableSpell  = function() return true, false end

_cd = {}
GetSpellCooldown = function(n)
  if _cd[tostring(n)] then return 995, 10 end  -- 5s pozostalo przy GetTime=1000
  return 0, 0
end
"""

AURA_ENV = """
aura_env = {prev={}, readyAt={}, auras={
  ["Devotion Aura"]=1,["Retribution Aura"]=1,["Concentration Aura"]=1,
  ["Shadow Resistance Aura"]=1,["Frost Resistance Aura"]=1,
  ["Fire Resistance Aura"]=1,["Crusader Aura"]=1,["Sanctity Aura"]=1
}}
"""

def make_unit_buff(buffs):
    lines = ["UnitBuff=function(unit,i)", "  if unit=='player' then"]
    for i, name in enumerate(buffs, 1):
        lines.append(f'    if i=={i} then return "{name}","","" end')
    return "\n".join(lines + ["  end", "  return nil", "end"])

def make_unit_debuff(debuffs):
    lines = ["UnitDebuff=function(unit,i)"]
    for i, name in enumerate(debuffs, 1):
        lines.append(f'  if unit=="target" and i=={i} then return "{name}","","",1,0,30,1030 end')
    return "\n".join(lines + ["  return nil", "end"])

def run_scenario(label, player_buffs=(), target_debuffs=(), spells_on_cd=()):
    """
    Zwraca liste wyswietlanych slotow: [{name, grey}]
    grey = allstates[""].needseal (jak push() ustawil e.grey)
    """
    slots = []
    for c_idx in DISPLAY_SLOTS:
        lua, _ = wa._lua()
        g = lua.globals()
        lua.execute(BASE_STUBS)
        lua.execute(AURA_ENV)
        lua.execute(make_unit_buff(player_buffs))
        lua.execute(make_unit_debuff(target_debuffs))
        for sp in spells_on_cd:
            lua.execute(f'_cd["{sp}"]=true')
        g._tsu = TSU[c_idx]
        lua.execute("local fn=load('return '.._tsu)(); local s={}; fn(s); _s=s['']")
        show = bool(lua.eval("_s and _s.show or false"))
        if show:
            slots.append({
                'name': str(lua.eval("_s.name or ''")),
                'grey': bool(lua.eval("_s.needseal or false")),
            })

    print(f"[{label}]")
    for i, s in enumerate(slots, 1):
        g_mark = " << SZARY" if s['grey'] else ""
        print(f"  slot{i}: {s['name']}{g_mark}")
    if not slots:
        print("  (kolejka pusta)")
    return slots

# ---------------------------------------------------------------------------
passes = 0
fails  = 0

def ok_check(cond, msg):
    global passes, fails
    if cond:
        print(f"  OK   {msg}")
        passes += 1
    else:
        print(f"  FAIL {msg}")
        fails += 1

# ---------------------------------------------------------------------------
# Scenariusz 1: Tier B, SoC + JotC + Judge ready → Judge NIE szary
# ---------------------------------------------------------------------------
q = run_scenario(
    "1: SoC + JotC + Judge ready",
    player_buffs=["Seal of Command", "Retribution Aura", "Blessing of Might"],
    target_debuffs=["Judgement of the Crusader"],
)
judge = next((e for e in q if "Judgement" in e['name']), None)
ok_check(judge is not None,            "Judge jest w wyswietlanych slotach")
ok_check(judge and not judge['grey'],  "Judge NIE jest szary [regresja: not curSeal, Tier A]")

# ---------------------------------------------------------------------------
# Scenariusz 2: Tier B, SoV (twistUp=true) + JotC + Judge ready → NIE szary
# To byl glowny bug (v3.9.1 regresja): not twistUp powodowalo szary Judge z SoC
# ---------------------------------------------------------------------------
q = run_scenario(
    "2: SoV (twistUp) + JotC + Judge ready  [glowna regresja v3.9.1]",
    player_buffs=["Seal of Vengeance", "Retribution Aura", "Blessing of Might"],
    target_debuffs=["Judgement of the Crusader"],
)
judge = next((e for e in q if "Judgement" in e['name']), None)
ok_check(judge is not None,            "Judge jest w wyswietlanych slotach z SoV")
ok_check(judge and not judge['grey'],  "Judge NIE jest szary z SoV [regresja: not twistUp, Tier B]")

# ---------------------------------------------------------------------------
# Scenariusz 3: Tier B, SoC + JotC + Judge NA CD → Judge poza slotami
# ---------------------------------------------------------------------------
q = run_scenario(
    "3: SoC + JotC + Judge na CD",
    player_buffs=["Seal of Command", "Retribution Aura", "Blessing of Might"],
    target_debuffs=["Judgement of the Crusader"],
    spells_on_cd=["Judgement"],
)
judge = next((e for e in q if "Judgement" in e['name']), None)
ok_check(judge is None, "Judge poza slotami gdy na CD [P8 cs==ready dziala]")

# ---------------------------------------------------------------------------
# Scenariusz 4: Opener — brak seala + brak JotC → SotC w slot 1
# ---------------------------------------------------------------------------
q = run_scenario(
    "4: Opener — brak seala, brak JotC",
    player_buffs=["Retribution Aura", "Blessing of Might"],
    target_debuffs=[],
)
ok_check(
    bool(q) and "Crusader" in q[0]['name'],
    f"Opener: slot1 = SotC (got: {q[0]['name'] if q else 'brak'})"
)

# ---------------------------------------------------------------------------
# Scenariusz 5: Opener — SotC aktywny + brak JotC → Judge w slot 1
# ---------------------------------------------------------------------------
q = run_scenario(
    "5: Opener — SotC aktywny, brak JotC",
    player_buffs=["Seal of the Crusader", "Retribution Aura", "Blessing of Might"],
    target_debuffs=[],
)
ok_check(
    bool(q) and "Judgement" in q[0]['name'],
    f"Opener: slot1 = Judge gdy SotC aktywny (got: {q[0]['name'] if q else 'brak'})"
)

# ---------------------------------------------------------------------------
print(f"\n{'='*50}")
print(f"Wynik: {passes} OK / {passes+fails} scenariuszy")
if fails:
    print(f"FAIL: {fails} nie przeszlo")
    raise SystemExit(1)
print("Wszystkie scenariusze OK")
