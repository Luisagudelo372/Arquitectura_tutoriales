from decimal import Decimal

from django.db import transaction
from django.shortcuts import get_object_or_404

from .domain.builders import OrdenBuilder
from .domain.logic import CalculadorImpuestos
from .models import Inventario, Libro, Orden



class CompraRapidaService:
    """
    SERVICE LAYER: Orquesta la interacción entre el dominio,
    la infraestructura y la base de datos.
    """

    def __init__(self, procesador_pago):
        self.procesador_pago = procesador_pago
        self.builder = OrdenBuilder()
        
    def ejecutar_proceso_compra(self, usuario, lista_productos, direccion):
    
    # Uso del Builder: Semántica clara y validación interna
        orden = (self.builder
                 .con_usuario(usuario)
                 .con_productos(lista_productos)
                 .para_envio(direccion)
                 .build())

    # Uso del Factory (inyectado): Cambio de comportamiento sin cambio de código
        if self.procesador_pago.pagar(orden.total):
            return f"Orden {orden.id} procesada exitosamente."
 
        orden.delete()
        raise Exception("Error en la pasarela de pagos.")


    def obtener_detalle_producto(self, libro_id):
        libro = get_object_or_404(Libro, id=libro_id)
        total = CalculadorImpuestos.obtener_total_con_iva(libro.precio)
        return {"libro": libro, "total": total}
    
    def procesar(self, libro_id):
        libro = Libro.objects.get(id=libro_id)
        inv = Inventario.objects.get(libro=libro)

        if inv.cantidad <= 0:
            raise ValueError("No hay existencias.")
        total = CalculadorImpuestos.obtener_total_con_iva(libro.precio)
        if self.procesador_pago.pagar(total):
            inv.cantidad -= 1
            inv.save()
            return total
        return None

    @transaction.atomic
    def procesar_compra_api(self, libro_id, cantidad, direccion, usuario=None):
        libro = Libro.objects.select_for_update().get(id=libro_id)
        inv = Inventario.objects.select_for_update().get(libro=libro)

        if inv.cantidad < cantidad:
            raise ValueError("Stock insuficiente para completar la compra.")

        precio_unitario = Decimal(str(libro.precio))
        subtotal = precio_unitario * cantidad
        total = Decimal(str(CalculadorImpuestos.obtener_total_con_iva(subtotal)))

        if not self.procesador_pago.pagar(float(total)):
            raise Exception("Error en la pasarela de pagos.")

        inv.cantidad -= cantidad
        inv.save()

        nueva_orden = Orden.objects.create(
            usuario=usuario if getattr(usuario, "is_authenticated", False) else None,
            libro=libro,
            total=total,
            direccion_envio=direccion,
        )
        return nueva_orden

    