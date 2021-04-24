from rest_framework.views import APIView, Response
from rest_framework import status

from ecomapp import serializers, models
class UserApiView(APIView):
    serializer_class = serializers.UserSerializer
    def get(self, reuest):
        obj = models.User.objects.all()
        serializer = self.serializer_class(obj, many=True)
        return Response(serializer.data)
    # def post(self, request):
    #     serializer = self.serializer_class(data = request.data)
    #     if serializer.is_valid()

class CategoryApiView(APIView):
    serializer_class = serializers.CategorySerializer
    def get(self, reuest):
        obj = models.Category.objects.all()
        serializer = self.serializer_class(obj, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            msg = f'Created Successfull'
            return Response({"message": msg})
        else:
            return Response({
                serializer.error,
                status.HTTP_400.BAD_REQUEST
            })

class CategoryApi(APIView):
    serializer_class = serializers.CategorySerializer
    def get_object(self, pk):
        try:
            return models.Category.objects.get(pk=pk)
        except models.Category.DoesNotExits:
            return Response({'Message': "The Category does not Exits"})
    
    def get(self,request, pk):
        categories = self.get_object(pk)
        serializer = self.serializer_class(categories)
        return Response(serializer.data)
    def put(self, request, pk):
        categories = self.get_object(pk)
        serializer = self.serializer_class(categories,data = request.data)
        if serializer.is_valid():
            serializer.save()
            msg = f'Created Successfull'
            return Response({"message": msg})
        return Response({
                serializer.error,
                status.HTTP_400.BAD_REQUEST
            })
            