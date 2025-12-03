import hashlib
import os
import tempfile
import uuid

from flask import Flask, abort, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename  # removes unsafe symbols from filenamee
from werkzeug.datastructures.file_storage import FileStorage


# Use absolute path to ensure the right folder path
BASE_FOLDER = os.path.abspath(os.path.dirname(__file__))
# write uploads outside the root folder for safety
UPLOAD_FOLDER = os.path.join(BASE_FOLDER, '..', 'uploads')

# Files
MAX_SIZE = 5 * 1024 * 1024  # 5 MB
CHUNK_SIZE_BYTES = 1 * 1024  # 1 KB

# CONFIGURATION
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_SIZE
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Allowed picture attributes
ALLOWED_EXT = {
    'png': {
        'soi': b'\x89PNG\r\n\x1a\n',
        'eoi': b''
    },
    'jpg': {
        'soi': b'\xff\xd8',            # Start Of Image (SOI)
        'eoi': b'\xff\xd9'             # End Of Image (EOI)
    },
    'gif': {
        'soi87a': b'GIF87a',           # GIF87a
        'soi89a': b'GIF89a',           # GIF89a
        'eoi': b''
    }
}

EXT_ALIASES = {
    'jpeg': 'jpg',
    'tif': 'tiff',
}

def normalize_ext(ext: str) -> str:
    """Zwraca znormalizowane rozszerzenie pliku."""
    ext = ext.lower()
    return EXT_ALIASES.get(ext, ext)


# UPLOAD VERIFICATION METHODS
def get_sigs(ext: str) -> tuple[list[bytes], bytes]:
    '''For given `ext`, get the list of SOI *bytes* **string**, and the EOI *bytes*.'''
    ext = normalize_ext(ext)
    ext_sigs = ALLOWED_EXT.get(ext, {})

    sois = [val for key, val in ext_sigs.items() if key.startswith("soi")]
    eoi = ext_sigs.get("eoi")

    return sois, eoi

def is_ext_allowed(filename: str) -> bool:
    if '.' in filename:
        ext = filename.rsplit('.', 1)[1].lower()
        ext = normalize_ext(ext)
        return ext in ALLOWED_EXT, ext
    else:
        return False, None

def _cleanup_413(tmp: tempfile._TemporaryFileWrapper, msg):
    tmp.close()
    if os.path.exists(tmp.name):
        os.remove(tmp.name)
    return abort(413, msg)

def handle_upload(file_storage):
    file_storage: FileStorage = file_storage
    total = 0
    sha = hashlib.sha256()
    first_bytes = b''
    last_bytes = b''
    tmp_name = None

    # First verify the extension
    app.logger.debug("Verifying the extension")
    ok, ext = is_ext_allowed(file_storage.filename)
    if not ok or not ext:
        abort(415, "Extension not allowed")
    else:
        app.logger.debug('Verification ok.')
    soi_signatures, eoi_signature = get_sigs(ext)
    # Get max length of signature start and end
    sig_start_len, sig_end_len = max([len(s) for s in soi_signatures]), len(eoi_signature)
    
    try:
        app.logger.debug('Creating temporary file')
        # Create temp file for further validation (don't delete on close, will do later)
        with tempfile.NamedTemporaryFile(dir=app.config['UPLOAD_FOLDER'],
                                         delete=False) as tmp:
            tmp_name = tmp.name

            # stream read by chunk
            app.logger.debug("Reading chunk by chunk...")
            while True:
                chunk = file_storage.stream.read(CHUNK_SIZE_BYTES)
                if not chunk:
                    app.logger.debug("Stream ended")
                    break
                
                # update the last bytes buffer
                if sig_end_len:
                    last_bytes = (last_bytes + chunk)[-sig_end_len:]
                
                total += len(chunk)
                if total > MAX_SIZE:
                    _cleanup_413(tmp, "File too large")

                # update SOI bytes until enough, then validate immediately
                if len(first_bytes) < sig_start_len:
                    need = sig_start_len - len(first_bytes)
                    first_bytes += chunk[:need]
                    if len(first_bytes) >= sig_start_len:
                        app.logger.debug("Verifying header...")
                        if not any(first_bytes.startswith(soi) for soi in soi_signatures):
                            _cleanup_413(tmp, f"Corrupted signature of {ext} file.")
                        else:
                            app.logger.debug("Verification ok.")
                
                tmp.write(chunk)
                sha.update(chunk)
            
            # closes the tmp file without deleting, now validate the SOI and readability
        app.logger.debug('Temporary file written and closed.')

        # Not conform to expected end of file (if sig_end_len=0, no verification required)
        if sig_end_len and last_bytes != eoi_signature:
            _cleanup_413(tmp, f"Corrupted signature of {ext} file.")
        
        # Check if file opens
        if ext in ALLOWED_EXT:  # if picture
            from PIL import Image
            try:
                Image.open(tmp_name).verify()
            except Exception:
                abort(422, "Cannot process the file")
        
        # Generate unique name and replace the temporary filename with the final one
        ext = os.path.splitext(secure_filename(file_storage.filename))[1]
        final = f"{uuid.uuid4().hex}{ext}"
        final_path = os.path.join(app.config['UPLOAD_FOLDER'], final)
        os.replace(tmp_name, final_path)
        os.chmod(final_path, 0o640)  # make it read/write only

        return final, total, sha.hexdigest()

    except Exception:
        # make sure to remove temporary file if it still exists
        if tmp_name and os.path.exists(tmp_name):
            try:
                os.remove(tmp_name)
            except Exception:
                pass
        raise

@app.route("/images/", methods=["GET", "POST"])
def form_view():
    if request.method == "POST":
        # verify form
        if 'file' not in request.files:
            return "no file part in the form", 400
        file = request.files['file']
        if file.filename == '':
            return 'no file selected', 400
        
        fname, size_bytes, sha =  handle_upload(file)
        app.logger.info(f"UPLOADED: {fname}, size: {size_bytes} B, sha: {sha}")
        return redirect(url_for("form_view"))
    
    return render_template('form_with_image.html')

if __name__ == '__main__':
    app.run(debug=True)
    