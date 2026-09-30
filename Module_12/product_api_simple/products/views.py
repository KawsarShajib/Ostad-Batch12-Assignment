
from rest_framework.generics import ListCreateAPIView
# ListCreateAPIView : because we need two operations (GET, POST) on the same endpoint:

from .models import Product
from .serializers import ProductSerializer


class ProductListCreateView(ListCreateAPIView):
    queryset = Product.objects.all().order_by('id')
    # gets all products and orders them by ID.
    serializer_class = ProductSerializer