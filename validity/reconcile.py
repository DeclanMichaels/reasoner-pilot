#!/usr/bin/env python3
"""Classify the validity/ working copy against a restored archive. Read-only, stdlib only.

Four buckets per data directory, and the exit code says whether anything is at risk:

  identical     same name, same sha256 as the archive
  differs       same name, different content            -> STOP
  recoverable   not in the archive, but byte-identical to a file tracked in git
  nowhere       not in the archive and not in git       -> STOP

Archive-only files are counted for information. Nothing under validity/ is written.
The audit scripts rewrite tracked outputs to match whatever data they see, so run this
before any sync into validity/ and again after; a clean exit from an audit says nothing
about whether the right data was present (docs/DEVELOPMENT_NOTES.md). Issue #5.

    python3 validity/reconcile.py --archive /tmp/restore            # working copy = validity/
    python3 validity/reconcile.py --archive /tmp/restore --working /path/to/validity

Exit 0 = reconciled; 1 = a stop bucket is non-empty; 2 = usage.
"""
import argparse, hashlib, subprocess, sys
from pathlib import Path

DIRS = ["runs", "runs_framed", "runs_framed_lang", "instruments"]
HERE = Path(__file__).resolve().parent


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def archive_hashes(archive):
    """relpath -> sha256. From ARCHIVE_MANIFEST.sha256 when present, else by hashing."""
    man = archive / "ARCHIVE_MANIFEST.sha256"
    out = {}
    if man.exists():
        for line in man.read_text().splitlines():
            if not line.strip():
                continue
            digest, rel = line.split(None, 1)
            out[rel.strip().lstrip("*").lstrip("./")] = digest
        return out
    for d in DIRS:
        for p in sorted((archive / d).glob("*")):
            if p.is_file():
                out["%s/%s" % (d, p.name)] = sha256(p)
    return out


def tracked_hashes(inside):
    """sha256 of every file git tracks in the repository containing `inside`, as a set."""
    top = subprocess.run(["git", "-C", str(inside), "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True, check=True).stdout.strip()
    repo = Path(top)
    ls = subprocess.run(["git", "-C", str(repo), "ls-files", "-z"], capture_output=True, check=True)
    hashes = set()
    for rel in ls.stdout.decode().split("\0"):
        if rel:
            p = repo / rel
            if p.is_file():
                hashes.add(sha256(p))
    return hashes


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--archive", required=True, help="directory the archive was synced into")
    ap.add_argument("--working", default=str(HERE), help="the validity/ working copy (default: this script's directory)")
    a = ap.parse_args()
    archive, working = Path(a.archive).resolve(), Path(a.working).resolve()
    if not archive.is_dir() or not working.is_dir():
        sys.exit(2)
    arch = archive_hashes(archive)
    if not arch:
        print("no archive files found under %s" % archive); sys.exit(2)
    tracked = tracked_hashes(working)

    stop = False
    print("working copy %s against archive %s (%d archive files)\n" % (working, archive, len(arch)))
    print("%-18s %10s %8s %12s %8s %13s" % ("directory", "identical", "differs", "recoverable", "nowhere", "archive-only"))
    listing = []
    totals = dict(identical=0, differs=0, recoverable=0, nowhere=0, archive_only=0)
    for d in DIRS:
        local = {p.name: p for p in (working / d).glob("*") if p.is_file()} if (working / d).is_dir() else {}
        in_arch = {rel[len(d) + 1:]: h for rel, h in arch.items() if rel.startswith(d + "/")}
        counts = dict(identical=0, differs=0, recoverable=0, nowhere=0)
        for name, p in sorted(local.items()):
            h = sha256(p)
            if name in in_arch:
                if h == in_arch[name]:
                    counts["identical"] += 1
                else:
                    counts["differs"] += 1; listing.append(("DIFFERS", "%s/%s" % (d, name)))
            elif h in tracked:
                counts["recoverable"] += 1
            else:
                counts["nowhere"] += 1; listing.append(("NOWHERE", "%s/%s" % (d, name)))
        archive_only = len(set(in_arch) - set(local))
        for k in counts:
            totals[k] += counts[k]
        totals["archive_only"] += archive_only
        print("%-18s %10d %8d %12d %8d %13d" % (d, counts["identical"], counts["differs"],
                                                counts["recoverable"], counts["nowhere"], archive_only))
    print("%-18s %10d %8d %12d %8d %13d" % ("total", totals["identical"], totals["differs"],
                                            totals["recoverable"], totals["nowhere"], totals["archive_only"]))
    for kind, rel in listing:
        print("  %-8s %s" % (kind, rel))
    stop = totals["differs"] > 0 or totals["nowhere"] > 0
    print()
    if stop:
        print("STOP: %d file(s) differ from the archive and %d exist nowhere else. Nothing was written."
              % (totals["differs"], totals["nowhere"]))
        sys.exit(1)
    print("RECONCILED: every local file is in the archive or in git. %d archive file(s) are not in the working copy."
          % totals["archive_only"])


if __name__ == "__main__":
    main()
