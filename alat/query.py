#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pretraga kataloga frontend literature.
Primjeri:
  python query.py --category anim-gsap-mastery --level expert
  python query.py --tag scrolltrigger --access free
  python query.py --search "view transitions" --gold
  python query.py --list-categories
"""
import json, os, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "katalog")

def load(gold=False):
    fn = "frontend_literature_gold.jsonl" if gold else "frontend_literature.jsonl"
    p = os.path.join(DATA, fn)
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--category")
    ap.add_argument("--level")
    ap.add_argument("--access")
    ap.add_argument("--type")
    ap.add_argument("--tag")
    ap.add_argument("--search")
    ap.add_argument("--gold", action="store_true", help="samo verified gold")
    ap.add_argument("--limit", type=int, default=50)
    ap.add_argument("--list-categories", action="store_true")
    a = ap.parse_args()

    rows = load(a.gold)
    if a.list_categories:
        import collections
        for c, n in sorted(collections.Counter(e.get("category") for e in rows).items()):
            print(f"{n:4d}  {c}")
        return

    def keep(e):
        if a.category and e.get("category") != a.category: return False
        if a.level and e.get("level") != a.level: return False
        if a.access and e.get("access") != a.access: return False
        if a.type and e.get("type") != a.type: return False
        if a.tag and a.tag.lower() not in [t.lower() for t in (e.get("subtopics") or []) + (e.get("machine_tags") or [])]: return False
        if a.search:
            blob = (e.get("title", "") + " " + (e.get("description") or "") + " " + " ".join(e.get("authors") or [])).lower()
            if a.search.lower() not in blob: return False
        return True

    res = [e for e in rows if keep(e)]
    for e in res[:a.limit]:
        au = ", ".join(e.get("authors") or [])
        au = f" - {au}" if au else ""
        yr = f" ({e.get('year')})" if e.get("year") else ""
        meta = "/".join(str(x) for x in [e.get("type"), e.get("level"), e.get("access")] if x)
        print(f"- {e.get('title')}{au}{yr} [{meta}] {e.get('url')}")
    print(f"\n[{len(res)} rezultata, prikazano {min(len(res), a.limit)}]")

if __name__ == "__main__":
    main()
