from django.shortcuts import render, get_object_or_404
from django.views import View

from .infra.factories import PaymentFactory
from .services import CompraRapidaService
from  django .http import HttpResponse
from .models import Libro, Inventario, Orden
from .infra.factories import PaymentFactory
import datetime



class CompraRapidaView(View):
    """
    CBV: Vista Basada en Clases.
    Actúa como un "Portero": recibe la petición y delega al servicio.
    """

    template_name = 'tienda_app/compra.html'

    def get(self, request, libro_id):
        libro = get_object_or_404(Libro, id=libro_id)
        total = float(libro.precio) * 1.19
        return render(request, self.template_name, {'libro': libro, 'total': total})

    def post(self, request, libro_id):
          service = CompraRapidaService(PaymentFactory.get_processor())
          total = service.procesar(libro_id)
          return HttpResponse(f"Comprado via CBV: ${total}")
    
    def setup_service(self):
         gateway = PaymentFactory.get_processor()
         return CompraRapidaService(procesador_pago=gateway)
    