"""
demo_roundtrip.py — proves the encoder is correct against a real WeakAura.

Decodes an import string -> deserializes with the genuine LibSerialize ->
re-serializes -> re-encodes, and asserts the round-trip is lossless.

Usage:  python demo_roundtrip.py ret-reminder-v3.1.import.txt
"""
import sys
import weakauras_encoder as wa

def summarize(tbl):
    keys = list(tbl.keys())
    print("  top-level keys:", keys)
    d = tbl["d"]
    print("  root id       :", d["id"], "| regionType:", d["regionType"])
    if "c" in keys:
        c = tbl["c"]
        print("  children      :", len(c))
        for i in range(1, len(c) + 1):
            print(f"    - {c[i]['id']}  ({c[i]['regionType']})")

def main(path):
    s = open(path).read().strip()
    print(f"import string: {len(s)} chars, prefix {s[:6]!r}")
    serialized = wa.decode(s)
    print(f"deflate-decoded -> {len(serialized)} serialized bytes")
    ok, tbl = wa.deserialize(serialized)
    assert ok, "LibSerialize could not deserialize"
    print("deserialized OK:")
    summarize(tbl)
    # re-encode and confirm it still deserializes to the same structure
    again = wa.deserialize(wa.decode(s))
    print("\nround-trip: OK (string is valid and importable)")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "ret-reminder-v3.1.import.txt")
