from pathlib import Path
from uuid import uuid4

from flask import current_app
from werkzeug.utils import secure_filename

from ..common.exceptions import AppError


def allowed_file(filename):
    suffix = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return suffix in current_app.config["ALLOWED_EXTENSIONS"]


def save_upload_file(file_storage):
    if not file_storage or not file_storage.filename:
        raise AppError("请选择要上传的文件")
    if not allowed_file(file_storage.filename):
        raise AppError("文件类型不支持")

    original_name = file_storage.filename
    safe_name = secure_filename(original_name)
    suffix = safe_name.rsplit(".", 1)[-1].lower() if "." in safe_name else ""
    stored_name = f"{uuid4().hex}.{suffix}" if suffix else uuid4().hex
    upload_dir = Path(current_app.config["UPLOAD_FOLDER"])
    upload_dir.mkdir(parents=True, exist_ok=True)
    file_path = upload_dir / stored_name
    file_storage.save(file_path)

    return {
        "original_name": original_name,
        "stored_name": stored_name,
        "file_path": f"/api/reports/files/{stored_name}",
        "file_size": file_path.stat().st_size,
        "content_type": file_storage.content_type,
    }
