#!/usr/bin/env python3
"""Check that every translation of a working document matches its current source.

    python tools/check_translations.py            list missing and outdated translations
    python tools/check_translations.py --strict   also exit with an error if there are any

The project is written for people in nine languages: English, Chinese, Spanish, French,
German, Italian, Russian, Portuguese and Arabic. A working document is written in one of
them (its source) and translated into the others. Each translation starts with a line

    <!-- translation of docs/CURRENT_DESIGN.md, source sha256: <hash> -->

naming the source and the SHA-256 of the source text it was made from. When the source
changes, the translation is listed here as outdated until it is translated again. The
source always wins where the two differ. The foundation (README, MANIFESTO, REQUIREMENTS)
is not checked here: it never changes (see CORE.md).
"""

import argparse
import hashlib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANGS = ["en", "zh", "es", "fr", "de", "it", "ru", "pt", "ar"]
HEADER = re.compile(r"^<!-- translation of (\S+), source sha256: ([0-9a-f]{64}) -->")

# source file -> {language: translation file}; the source's own language is not listed
DOCS = {}
for name in ("CURRENT_DESIGN", "RESEARCH_AGENT", "PILOT_RESULTS", "OPEN_QUESTIONS", "BOARD", "ROADMAP", "THREAT_MODEL"):
    DOCS["docs/%s.md" % name] = dict(
        [("en", "docs/%s.en.md" % name)]
        + [(lang, "i18n/%s/%s.md" % (lang, name)) for lang in LANGS if lang not in ("en", "ru")])
DOCS["android/README.md"] = dict((lang, "i18n/%s/ANDROID.md" % lang) for lang in LANGS if lang != "en")
DOCS["installer/windows/README.md"] = dict((lang, "i18n/%s/WINDOWS_INSTALLER.md" % lang) for lang in LANGS if lang != "en")
DOCS["installer/linux/README.md"] = dict((lang, "i18n/%s/LINUX_INSTALLER.md" % lang) for lang in LANGS if lang != "en")
DOCS["docs/CONNECT.md"] = dict((lang, "i18n/%s/CONNECT.md" % lang) for lang in LANGS if lang != "en")
DOCS["tasks/context/variant-b.md"] = {"en": "tasks/context/variant-b.en.md"}
# English sources
for source, name in (("CORE.md", "CORE"), ("ERRATA.md", "ERRATA"), ("tasks/README.md", "TASKS"),
                     ("results/README.md", "RESULTS"), ("results/FIRST_RUN.md", "FIRST_RUN")):
    DOCS[source] = dict((lang, "i18n/%s/%s.md" % (lang, name)) for lang in LANGS if lang != "en")

# Pages written in all nine languages at once (no source/translation relation, nothing to stamp).
# The foundation (README, MANIFESTO, REQUIREMENTS) is among them and never changes after core-v1.
PARALLEL = {}
for name in ("README", "MANIFESTO", "REQUIREMENTS", "AGENTS", "CONTRIBUTING"):
    PARALLEL[name] = dict([("en", "%s.md" % name)]
                          + [(lang, "i18n/%s/%s.md" % (lang, name)) for lang in LANGS if lang != "en"])
PARALLEL["AGENT"] = dict([("en", "agent/README.md")]
                         + [(lang, "i18n/%s/AGENT.md" % lang) for lang in LANGS if lang != "en"])


def source_language(source):
    """Language a tracked source document is written in."""
    english = ("android/README.md", "installer/windows/README.md", "installer/linux/README.md", "docs/CONNECT.md", "CORE.md", "ERRATA.md", "tasks/README.md", "results/README.md",
               "results/FIRST_RUN.md")
    return "en" if source in english else "ru"


def sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def check(root):
    """Return a list of (kind, file, detail)."""
    problems = []
    for source, translations in sorted(DOCS.items()):
        src_path = os.path.join(root, *source.split("/"))
        if not os.path.exists(src_path):
            problems.append(("missing source", source, ""))
            continue
        current = sha(src_path)
        for lang, target in sorted(translations.items()):
            path = os.path.join(root, *target.split("/"))
            if not os.path.exists(path):
                problems.append(("missing", target, "translation of %s into %s" % (source, lang)))
                continue
            with open(path, encoding="utf-8") as f:
                first = f.readline().strip()
            m = HEADER.match(first)
            if not m or m.group(1) != source:
                problems.append(("no header", target, "the first line must name %s and its hash" % source))
            elif m.group(2) != current:
                problems.append(("outdated", target, "%s changed after this translation" % source))
    return problems


def header(source, root):
    return "<!-- translation of %s, source sha256: %s -->" % (source, sha(os.path.join(root, *source.split("/"))))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", default=os.path.join(HERE, ".."))
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args(argv)
    problems = check(os.path.abspath(args.root))
    for kind, path, detail in problems:
        print("%-14s %s  %s" % (kind, path, detail))
    if not problems:
        print("All translations match their sources.")
    return 1 if problems and args.strict else 0


if __name__ == "__main__":
    sys.exit(main())
