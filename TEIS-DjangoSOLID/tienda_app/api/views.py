from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from tienda_app.infra.factories import PaymentFactory
from tienda_app.services import CompraRapidaService
from .serializers import OrdenInputSerializer



class CompraAPIView(APIView):
    """
    Endpoint para procesar compras via JSON.
    POST /api/v1/comprar/
    Payload: {"libro_id": 1, "direccion_envio": "Calle 123", "cantidad": 1}
    """

    def post(self, request):
        serializer = OrdenInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        datos = serializer.validated_data

        try:
            gateway = PaymentFactory.get_processor()
            servicio = CompraRapidaService(procesador_pago=gateway)
            orden = servicio.procesar_compra_api(
                libro_id=datos['libro_id'],
                cantidad=datos['cantidad'],
                direccion=datos['direccion_envio'],
                usuario=request.user
            )

            return Response(
                {
                    'estado': 'exito',
                    'mensaje': 'Orden creada correctamente.',
                    'orden_id': orden.id,
                    'total': str(orden.total),
                },
                status=status.HTTP_201_CREATED,
            )

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_409_CONFLICT)
        except Exception:
            return Response({'error': 'Error interno'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
