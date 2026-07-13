from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response # BU SATIRI EKLE
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Kitap
from .serializers import KitapSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly]) 
def kitap_listesi(request):
    if request.method == 'GET':
        serializer = KitapSerializer(Kitap.objects.all(), many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = KitapSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def kitap_detay(request, pk):
    kitap = get_object_or_404(Kitap, pk=pk)
    if request.method == 'GET':
        return Response(KitapSerializer(kitap).data)
    elif request.method == 'PUT':
        serializer = KitapSerializer(kitap, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        kitap.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)