from flask import Blueprint, Response, json

from password_wallet import ic
from password_wallet.encryptions import info

bp = Blueprint("encryption", __name__, url_prefix="/encryption")

@bp.get("info/<encryption_method_name>")
def encryption_info(encryption_method_name: str):
    info_data = info(encryption_method_name)
    if not info_data:
        ic(f"Nie znalezione informacji o metodzie szyfrowania: {encryption_method_name}")
        return Response(json.dumps({
            "type": "error",
            "message": "Nie znaleziono metody szyfrowania"
        }),
        status=404)
    
    ic(f"Pobrano informacje o metodzie szyfrowania: {encryption_method_name} Info: {info_data}")
    return Response(json.dumps(info_data), status=200)

ic(f"Załadowano moduł: {__name__}")