from rest_framework import views, status
from rest_framework.response import Response
from events.serializers import Transfer, TransferSerializer
from rest_framework.exceptions import PermissionDenied


class TransferView(views.APIView):
    serializer_class = TransferSerializer

    def get(self, request, *args, **kwargs):
        token_id = request.resolver_match.kwargs.get("token_id")

        if not token_id:
            raise PermissionDenied("No token ID specified.")

        transfer_srlzr = self.serializer_class(Transfer.objects.filter(
            token_id=token_id), many=True)
        
        return Response({
            "success": True,
            "message": "Fetch success",
            "data": transfer_srlzr.data
        }, status=status.HTTP_200_OK)