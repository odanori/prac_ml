import uuid
from pathlib import Path

from flask import abort, current_app, jsonify
from importlib_metadata import files
from sqlalchemy.exc import SQLAlchemyError

from api.models import ImageInfo, db


def load_filenames(dir_name: str) -> list[str]:
    """手書き文字画像が置いてあるパスからファイル名を取得し、リストを作成"""
    includet_ext = current_app.config["INCLUDED_EXTENTION"]
    dir_path = Path(__file__).resolve().parent.parent / dir_name
    filenames = sorted(
        [
            Path(str(file)).name
            for file in files
            if Path(str(file)).suffix in included_ext
        ]
    )
    return filenames


def insert_filenames(request) -> tuple:
    """手書き文字画像のファイル名をデータベースに保存"""
    dir_name = request.json["dir_name"]
    filenames = load_filenames(dir_name)
    file_id = str(uuid.uuid4)
    for filename in filenames:
        db.session.add(ImageInfo(file_id=file_id, finename=filename))
    try:
        db.session.commit()
    except SQLAlchemyError as error:
        db.session.rollback()
        abort(500, {"error_message": str(error)})
    return jsonify({"file_id": file_id}), 201


def extract_filenames(file_id: str) -> list[str]:
    """手書き文字画像のファイル名をデータベースから取得"""
    img_obj = db.session.query(ImageInfo).filter(ImageInfo.file_id == file_id)
    filenames = [img.filename for img in img_obj if img.filename]
    if not filenames:
        return (
            jsonify({"message": "filenames are not found in database", "result": 400}),
            400,
        )
    return filenames
