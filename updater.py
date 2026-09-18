"""
Mises à jour à distance pour OPTILUX Desktop.

Télécharge un manifeste JSON, compare les versions, et applique la mise à jour
si une version plus récente est disponible. Ne touche JAMAIS aux données :
optilux.db, factures/, assets/products/, assets/factures_stockees/.
"""
import os
import sys
import json
import shutil
import zipfile
import tempfile
import urllib.request
from tkinter import messagebox

# Files/dirs the updater will never overwrite.
PROTECTED = {
    "optilux.db",
    "optilux.db-journal",
    "factures",
    os.path.join("assets", "products"),
    os.path.join("assets", "factures_stockees"),
    ".git",
    "__pycache__",
}


def _parse_version(v):
    """'1.2.3' → (1, 2, 3). Non-numeric parts become 0."""
    out = []
    for part in str(v).split("."):
        try:
            out.append(int(part))
        except ValueError:
            out.append(0)
    return tuple(out)


def check_for_update(manifest_url, current_version, timeout=6):
    """Returns a dict {'version', 'url', 'notes', 'mandatory'} if a newer
    version is available, else None. Raises on network error."""
    req = urllib.request.Request(manifest_url, headers={"User-Agent": "Optilux-Updater/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    if _parse_version(data["version"]) <= _parse_version(current_version):
        return None
    return data


def download_and_apply(info, app_dir):
    """Download the zip in info['url'], extract it, and copy updated source
    files into app_dir (skipping protected paths). Returns the count of files
    replaced."""
    tmp_dir = tempfile.mkdtemp(prefix="optilux_update_")
    zip_path = os.path.join(tmp_dir, "update.zip")

    try:
        req = urllib.request.Request(info["url"], headers={"User-Agent": "Optilux-Updater/1.0"})
        with urllib.request.urlopen(req, timeout=60) as resp, open(zip_path, "wb") as f:
            shutil.copyfileobj(resp, f)

        extract_dir = os.path.join(tmp_dir, "extracted")
        os.makedirs(extract_dir, exist_ok=True)
        with zipfile.ZipFile(zip_path) as z:
            z.extractall(extract_dir)

        # The zip may contain a top-level folder (e.g. optilux-1.1.0/).
        # Detect and descend into it.
        entries = [e for e in os.listdir(extract_dir) if not e.startswith("__MACOSX")]
        src_root = extract_dir
        if len(entries) == 1 and os.path.isdir(os.path.join(extract_dir, entries[0])):
            src_root = os.path.join(extract_dir, entries[0])

        replaced = 0
        for root, dirs, files in os.walk(src_root):
            rel = os.path.relpath(root, src_root)
            # Skip protected directories at any depth
            dirs[:] = [d for d in dirs if not _is_protected(os.path.join(rel, d) if rel != "." else d)]

            for name in files:
                rel_path = os.path.join(rel, name) if rel != "." else name
                if _is_protected(rel_path):
                    continue
                # Only update source & assets; skip anything data-ish.
                if not _is_updatable(rel_path):
                    continue
                src = os.path.join(root, name)
                dst = os.path.join(app_dir, rel_path)
                os.makedirs(os.path.dirname(dst), exist_ok=True) if os.path.dirname(dst) else None
                shutil.copy2(src, dst)
                replaced += 1

        return replaced
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def _is_protected(rel_path):
    norm = os.path.normpath(rel_path).replace("\\", "/")
    for p in PROTECTED:
        p_norm = os.path.normpath(p).replace("\\", "/")
        if norm == p_norm or norm.startswith(p_norm + "/"):
            return True
    return False


def _is_updatable(rel_path):
    """Only .py, .docx, .ico, .png, .txt, .json, .md files are copied."""
    ext = os.path.splitext(rel_path)[1].lower()
    return ext in (".py", ".docx", ".ico", ".png", ".txt", ".json", ".md")