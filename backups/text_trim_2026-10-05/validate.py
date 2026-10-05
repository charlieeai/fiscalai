"""Validate shortened texts before they are written to the Omaha Value DB.

Input: a JSON list of {"table","id","column","old","new","limit"}.
Fails (exit 1) when a rewrite is empty, longer than its limit or than the
original, or contains a number that is not in the original text.
"""
import json
import re
import sys

NUM = re.compile(r"\d+(?:[.,]\d+)*")


def numbers(text: str) -> set[str]:
    return {n.replace(",", "") for n in NUM.findall(text or "")}


def words(text: str) -> int:
    return len((text or "").split())


def main(path: str) -> int:
    rows = json.load(open(path))
    bad = []
    for r in rows:
        new, old, limit = r.get("new", ""), r.get("old", ""), int(r["limit"])
        problems = []
        if not new.strip():
            problems.append("empty")
        if words(new) > limit:
            problems.append(f"{words(new)} words > {limit}")
        if words(new) > words(old):
            problems.append("longer than original")
        invented = numbers(new) - numbers(old)
        if invented:
            problems.append(f"numbers not in original: {sorted(invented)}")
        if problems:
            bad.append({"table": r["table"], "id": r["id"], "column": r["column"], "problems": problems})
    print(json.dumps({"checked": len(rows), "failed": len(bad), "failures": bad}, ensure_ascii=False, indent=1))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
