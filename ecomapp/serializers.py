# from rest_framework import serializers
# from ecomapp import models

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.User
#         fields = '__all__'
#         extra_kwargs = {
#             'password': {
#                 'write_only': True,
#                 'style': {
#                     'input_type': 'password'
#                 }
#             }
#         }

# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Category
#         fields = '__all__'