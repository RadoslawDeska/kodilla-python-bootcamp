import os
import uuid
import hashlib
import tempfile
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from flask import current_app as app, abort
from PIL import Image


def normalize_ext(ext: str) -> str:
    ext = ext.lower()
    return app.config["EXT_ALIASES"].get(ext, ext)


def get_sigs(ext: str):
    ext = normalize_ext(ext)
    ext_sigs = app.config["ALLOWED_EXT"].get(ext, {})
    sois = [val for key, val in ext_sigs.items() if key.startswith("soi")]
    eoi = ext_sigs.get("eoi", b"")
    return sois, eoi


def is_ext_allowed(filename: str):
    if "." not in filename:
        return False, None
    ext = normalize_ext(filename.rsplit(".", 1)[1].lower())
    return ext in app.config["ALLOWED_EXT"], ext


def _cleanup_413(tmp, msg):
    tmp.close()
    if os.path.exists(tmp.name):
        os.remove(tmp.name)
    abort(413, msg)


def handle_upload(fs: FileStorage):
    MAX_SIZE = app.config["MAX_CONTENT_LENGTH"]
    CHUNK_SIZE_BYTES = app.config["CHUNK_SIZE_BYTES"]

    total = 0
    sha = hashlib.sha256()
    first_bytes = b""
    last_bytes = b""
    tmp_name = None

    if not fs.filename:
        abort(400, "No file selected")

    ok, ext = is_ext_allowed(fs.filename)
    if not ok:
        abort(415, "Extension not allowed")

    soi_signatures, eoi_signature = get_sigs(ext)
    sig_start_len = max(len(s) for s in soi_signatures)
    sig_end_len = len(eoi_signature)

    try:
        with tempfile.NamedTemporaryFile(
            dir=app.config["UPLOAD_FOLDER"], delete=False
        ) as tmp:
            tmp_name = tmp.name

            while True:
                chunk = fs.stream.read(CHUNK_SIZE_BYTES)
                if not chunk:
                    break

                if sig_end_len:
                    last_bytes = (last_bytes + chunk)[-sig_end_len:]

                total += len(chunk)
                if total > MAX_SIZE:
                    _cleanup_413(tmp, "File too large")

                if len(first_bytes) < sig_start_len:
                    need = sig_start_len - len(first_bytes)
                    first_bytes += chunk[:need]
                    if len(first_bytes) >= sig_start_len:
                        if not any(
                            first_bytes.startswith(soi)
                            for soi in soi_signatures
                        ):
                            _cleanup_413(
                                tmp, f"Corrupted signature of {ext} file."
                            )

                tmp.write(chunk)
                sha.update(chunk)

        if sig_end_len and last_bytes != eoi_signature:
            abort(413, f"Corrupted signature of {ext} file.")

        try:
            Image.open(tmp_name).verify()
        except Exception:
            abort(422, "Cannot process the file")

        ext = os.path.splitext(secure_filename(fs.filename))[1]
        final = f"{uuid.uuid4().hex}{ext}"
        final_path = os.path.join(app.config["UPLOAD_FOLDER"], final)
        os.replace(tmp_name, final_path)
        os.chmod(final_path, 0o640)

        return final, total, sha.hexdigest()

    except Exception:
        if tmp_name and os.path.exists(tmp_name):
            try:
                os.remove(tmp_name)
            except Exception:
                pass
        raise
