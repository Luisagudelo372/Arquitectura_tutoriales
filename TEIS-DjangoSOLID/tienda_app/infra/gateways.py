import datetime
from pathlib import Path

from ..domain.interfaces import ProcesadorPago


LOG_FILE_PATH = Path(__file__).resolve().parents[2] / "pagos_locales_LUIS_AGUDELO.log"


def registrar_pago(monto: float, proveedor: str) -> None:
    with open(LOG_FILE_PATH, "a", encoding="utf-8") as f:
        f.write(
            f"[{datetime.datetime.now()}] {proveedor}: Transaccion exitosa por ${monto}\n"
        )

class BancoNacionalProcesador(ProcesadorPago):
    """
    Implementación concreta de la infraestructura.
    Simula un banco local escribiendo en un log.
    """
    def pagar(self, monto: float) -> bool:
        registrar_pago(monto, "BANCO")
        return True 