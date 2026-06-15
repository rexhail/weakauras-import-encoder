# WeakAuras Import String Encoder

A small Python tool that builds importable WeakAuras strings (the `!WA:2!`
format you paste into the in-game Import box) without the game running.

It also ships a few ready-to-use auras I made for a TBC Retribution Paladin.

## How it works

A WeakAuras export string is just three steps stacked together:

1. the aura table is serialized with **LibSerialize**
2. the bytes are compressed with **DEFLATE**
3. the result is packed into printable text and prefixed with `!WA:2!`

This repo reproduces that exactly. LibSerialize is the real Lua library, run
through a Lua interpreter (`lupa`), so the output is byte-for-byte the same as
the game produces. DEFLATE uses Python's `zlib`, and the final packing is a
6-bit encoding over a fixed alphabet.

## Requirements

```
pip install lupa
```

`LibSerialize.lua` is downloaded automatically on first run.

## Usage

Decode an existing string back into a table:

```python
import weakauras_encoder as wa

data = wa.decode(open("seal-tracker.import.txt").read())
ok, table = wa.deserialize(data)
print(table["d"]["id"])
```

Build a string from a Lua table:

```python
import weakauras_encoder as wa

s = wa.encode_table('''
    return { d = { id = "Hello", regionType = "text" }, s = "5.21.2", v = 1421, m = "d" }
''')
print(s)  # !WA:2!....
```

Check that a string is valid:

```
python demo_roundtrip.py ret-reminder-v3.1.import.txt
```

## Auras included

Drop-in import strings for a TBC Anniversary Retribution Paladin. See
[AURAS.md](AURAS.md) for what each one does and how to import.

- `rexhail-rotation-ret.import.txt` — the main rotation helper: a live row of
  icons where the leftmost is what to press next (Seal → Hammer of Wrath execute
  → Crusader Strike → Judgement → Exorcism on Undead/Demon), plus a GCD bar and
  swing timer. The visible icons auto-center as they come and go. It detects any
  active seal, and when you run low on mana it suggests Seal of Wisdom, then
  switching back to your offensive seal once you recover. Published on wago:
  https://wago.io/f-ofmKAvL
- `ret-priority-queue.import.txt` — the earlier prototype of that rotation: a
  single icon driven by one dynamic group. Kept for reference.
- `ret-reminder-v3.1.import.txt` — Crusader Strike / Seal of Command / Judgement
  reminders, swing timer, GCD bar, and a Hammer of Wrath finisher.
- `seal-tracker.import.txt` — a standalone seal tracker.

## Credits

- [LibSerialize](https://github.com/rossnichols/LibSerialize) and
  [LibDeflate](https://github.com/SafeteeWoW/LibDeflate) — the serialization and
  compression libraries used by WeakAuras (both MIT-licensed).
- The Ret Paladin auras started from Baranor's
  [TBC Retribution Paladin](https://wago.io/kcu8bck8n) layout and were rebuilt
  and trimmed down from there.

## License

MIT. See [LICENSE](LICENSE).

---

Built with help from Claude (Anthropic) while figuring out the WeakAuras format.
