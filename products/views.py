from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Product
from .serializers import ProductSerializer
from .permissions import IsOwnerOrReadOnly
from .filters import ProductFilter


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter

    search_fields = ['name', 'brand', 'description']
    ordering_fields = ['created_at', 'price', 'year', 'name']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": "Product deleted successfully."},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'])
    def my_listings(self, request):
        """GET /api/products/my_listings/ — returns only your own listings"""
        if not request.user.is_authenticated:
            return Response(
                {"detail": "You must be logged in to view your listings."},
                status=status.HTTP_401_UNAUTHORIZED
            )
        my_products = Product.objects.filter(owner=request.user)
        serializer = self.get_serializer(my_products, many=True)
        return Response({"count": my_products.count(), "results": serializer.data})