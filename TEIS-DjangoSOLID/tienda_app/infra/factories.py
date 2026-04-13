import os
import logging


from .gateways import BancoNacionalProcesador, registrar_pago


class MockPaymentProcessor:
    def pagar(self, monto: float) -> bool:
        print(f"[DEBUG] Mock Payment: Procesando pago de ${monto} sin cargo real.")
        registrar_pago(monto, "MOCK")
        return True



class PaymentFactory:
    @staticmethod
    def get_processor():
        provider = os.getenv('PAYMENT_PROVIDER', 'BANCO').strip().upper()
        print("Proveedor de pago:", provider)

        if provider == 'MOCK':
            return MockPaymentProcessor()

        return BancoNacionalProcesador()

