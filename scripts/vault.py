#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Keep the teacher's files encrypted in the public repo.

    python scripts/vault.py seal       # lectureN/_teacher/*  ->  dashboard/vault/  (build_dashboard runs this)
    python scripts/vault.py open       # restore any missing _teacher file from the vault (a fresh clone)
    python scripts/vault.py password   # change the dashboard password from this machine

The repo is public, so lectureN/_teacher/ (answer keys, exams, model answers
not yet released) is kept out of git. What goes into git is
dashboard/vault/lectureN/<file>.enc, each file encrypted with AES-GCM under
one random key -- the same key that encrypts the dashboard page.

THE KEY AND THE PASSWORD
The key never changes. dashboard/lock.json holds it wrapped by the
password (PBKDF2-SHA256 -> AES-GCM), so changing the password -- here, or
from the dashboard on a phone -- rewrites that one small file and nothing
else. This machine keeps the key itself in scripts/.dashboard-key
(gitignored) so the builds need no password. If that file is lost, the
first build asks for the password and recovers the key from lock.json.

File format: 12 bytes of IV, then the ciphertext with its tag.
"""
import base64, getpass, json, os, sys
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import hashlib

ROOT = Path(__file__).resolve().parent.parent
KEYFILE = ROOT / "scripts" / ".dashboard-key"
FIRST_PASSWORD = ROOT / "scripts" / ".dashboard-password"   # read once, to make lock.json
LOCK = ROOT / "dashboard" / "lock.json"
VAULT = ROOT / "dashboard" / "vault"
ROUNDS = 310000                    # the dashboard's lock page reads this from lock.json

b64 = lambda b: base64.b64encode(b).decode("ascii")


def encrypt(key, data):
    iv = os.urandom(12)
    return iv + AESGCM(key).encrypt(iv, data, None)


def decrypt(key, blob):
    return AESGCM(key).decrypt(blob[:12], blob[12:], None)


def wrap(key, password):
    salt, iv = os.urandom(16), os.urandom(12)
    k = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, ROUNDS, 32)
    return {"v": 1, "rounds": ROUNDS, "salt": b64(salt), "iv": b64(iv),
            "key": b64(AESGCM(k).encrypt(iv, key, None))}


def unwrap(lock, password):
    k = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"),
                            base64.b64decode(lock["salt"]), lock["rounds"], 32)
    return AESGCM(k).decrypt(base64.b64decode(lock["iv"]), base64.b64decode(lock["key"]), None)


def write_lock(lock):
    LOCK.parent.mkdir(parents=True, exist_ok=True)
    LOCK.write_text(json.dumps(lock, indent=2) + "\n", encoding="utf-8", newline="\n")


def key():
    if KEYFILE.is_file():
        return base64.b64decode(KEYFILE.read_text().strip())
    if LOCK.is_file():
        lock = json.loads(LOCK.read_text(encoding="utf-8"))
        pw = os.environ.get("DASHBOARD_PASSWORD") or getpass.getpass("Dashboard password: ")
        try:
            k = unwrap(lock, pw)
        except Exception:
            raise SystemExit("wrong password for dashboard/lock.json")
    else:                          # the very first time: a new key, wrapped by the first password
        pw = os.environ.get("DASHBOARD_PASSWORD") or (
            FIRST_PASSWORD.read_text(encoding="utf-8").strip() if FIRST_PASSWORD.is_file() else "")
        if len(pw) < 8:
            raise SystemExit("put a password of 8+ characters in %s for the first build"
                             % FIRST_PASSWORD.relative_to(ROOT).as_posix())
        k = os.urandom(32)
        write_lock(wrap(k, pw))
    KEYFILE.write_text(b64(k) + "\n")
    return k


def vault_path(src):
    """lecture7/_teacher/x.html -> dashboard/vault/lecture7/x.html.enc (no
    underscore folder: Jekyll would not serve it)"""
    rel = src.relative_to(ROOT)
    return VAULT / rel.parts[0] / (rel.name + ".enc")


def seal(k=None):
    k = k or key()
    changed = 0
    for src in sorted(ROOT.glob("lecture*/_teacher/*")):
        if not src.is_file():
            continue
        dst, data = vault_path(src), src.read_bytes()
        if dst.is_file():
            try:
                if decrypt(k, dst.read_bytes()) == data:
                    continue               # unchanged: keep the old file, so git sees no change
            except Exception:
                pass
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(encrypt(k, data))
        changed += 1
    return changed


def unseal(k=None):
    k = k or key()
    restored = 0
    for enc in sorted(VAULT.glob("lecture*/*.enc")):
        src = ROOT / enc.parent.name / "_teacher" / enc.name[:-4]
        if not src.is_file():
            src.parent.mkdir(parents=True, exist_ok=True)
            src.write_bytes(decrypt(k, enc.read_bytes()))
            restored += 1
    return restored


def change_password():
    k = key()
    a = getpass.getpass("New dashboard password: ")
    if len(a) < 8 or a != getpass.getpass("Again: "):
        raise SystemExit("not changed: under 8 characters, or the two did not match")
    write_lock(wrap(k, a))
    print("dashboard/lock.json rewritten; commit and push it.")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "seal":
        print("%d file(s) sealed into %s" % (seal(), VAULT.relative_to(ROOT).as_posix()))
    elif cmd == "open":
        print("%d file(s) restored from the vault" % unseal())
    elif cmd == "password":
        change_password()
    else:
        raise SystemExit(__doc__)
