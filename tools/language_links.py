#!/usr/bin/env python3
"""Put the line with links to every language version under the title of each page.

    python tools/language_links.py           write the lines
    python tools/language_links.py --check   only report pages whose line is missing or wrong

The line looks the same everywhere, in the order English · 中文 · Español · Français ·
Deutsch · Italiano · Русский · Português · العربية, with the current language in bold and
only languages that exist as links. Run it after adding a translation. A translation that was
up to date stays up to date: when a source changes only by this line, the tool writes the new
source hash into its translations (see tools/check_translations.py).
"""

import argparse
import os
import posixpath
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check_translations as ct  # noqa: E402

NAMES = {"en": "English", "zh": "中文", "es": "Español", "fr": "Français", "de": "Deutsch", "it": "Italiano",
         "ru": "Русский", "pt": "Português", "ar": "العربية"}
ORDER = ["en", "zh", "es", "fr", "de", "it", "ru", "pt", "ar"]
OLD_MARK = " <!-- languages -->"


def groups():
    """Every page that exists in more than one language: [{lang: path}]."""
    out = [dict(v) for v in ct.PARALLEL.values()]
    for source, translations in ct.DOCS.items():
        versions = dict(translations)
        versions[ct.source_language(source)] = source
        out.append(versions)
    return out


def is_language_line(line):
    plain = line.replace(OLD_MARK, "")
    return (" · " in plain and ("English" in plain or "Русский" in plain)
            and ("Русский" in plain or "中文" in plain)) or plain.startswith("Translations:")


def wanted_line(versions, lang, path, root):
    here = posixpath.dirname(path)
    parts = []
    for l in ORDER:
        if l not in versions or not os.path.exists(os.path.join(root, *versions[l].split("/"))):
            continue
        if l == lang:
            parts.append("**%s**" % NAMES[l])
        else:
            parts.append("[%s](%s)" % (NAMES[l], posixpath.relpath(versions[l], here or ".")))
    return " · ".join(parts)


def apply(root, check_only=False):
    changed, wrong = [], []
    before = dict((s, ct.sha(os.path.join(root, *s.split("/")))) for s in ct.DOCS
                  if os.path.exists(os.path.join(root, *s.split("/"))))
    for versions in groups():
        present = [l for l in versions if os.path.exists(os.path.join(root, *versions[l].split("/")))]
        if len(present) < 2:
            continue
        for lang in present:
            path = versions[lang]
            full = os.path.join(root, *path.split("/"))
            with open(full, encoding="utf-8", newline="") as f:
                text = f.read()
            lines = text.split("\n")
            line = wanted_line(versions, lang, path, root)
            heading = next(i for i, l in enumerate(lines) if l.startswith("# "))
            existing = [i for i, l in enumerate(lines[:heading + 6]) if i > heading and is_language_line(l)]
            if existing and lines[existing[0]] == line and len(existing) == 1:
                continue
            wrong.append(path)
            if check_only:
                continue
            for i in reversed(existing):
                del lines[i]
            lines[heading + 1:heading + 1] = ["", line]
            new = "\n".join(lines)
            while "\n\n\n" in new:
                new = new.replace("\n\n\n", "\n\n")
            with open(full, "w", encoding="utf-8", newline="") as f:
                f.write(new)
            changed.append(path)
    if not check_only:
        # translations whose source just changed by this line: stamp them with the new source hash
        for source, translations in ct.DOCS.items():
            for path in translations.values():
                full = os.path.join(root, *path.split("/"))
                if not os.path.exists(full):
                    continue
                with open(full, encoding="utf-8") as f:
                    text = f.read()
                m = ct.HEADER.match(text)
                if m and source in changed and m.group(2) == before.get(source):
                    text = ct.header(source, root) + "\n" + text.split("\n", 1)[1]
                    with open(full, "w", encoding="utf-8", newline="\n") as f:
                        f.write(text)
    return wrong


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", default=os.path.join(HERE, ".."))
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    wrong = apply(os.path.abspath(args.root), args.check)
    for path in wrong:
        print(("missing or wrong: " if args.check else "updated: ") + path)
    if not wrong:
        print("Every page has its language line.")
    return 1 if wrong and args.check else 0


if __name__ == "__main__":
    sys.exit(main())
