from django.shortcuts import render
import requests
import json
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from .models import Users
from .serializers import UserSerializer, InputSerializer


class InputViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = InputSerializer(data=request.data)
        if serializer.is_valid():
            INN = serializer.validated_data['INN']
            UKEP = serializer.validated_data['UKEP']
            MCHD = serializer.validated_data['MCHD']
            email = serializer.validated_data['email']

            # Validating INN by api-fns

            url = 'https://api-fns.ru/api/egr'
            params = {
                'req': INN,
                'key': '90bc98530dabe4d2d36c8082223e8efc56382a1f'
            }

            response = requests.get(url, params=params)

            value = ""
            if response.status_code == 200:
                data = response.json()
                value = data["items"][0]["ЮЛ"]["Руководитель"]

            if value != "":
                user_data = {'email': email, 'verified': True}
                user_serializer = UserSerializer(data=user_data)
                if user_serializer.is_valid():
                    response = requests.post('http://localhost:8000/api/users/', data=user_serializer.data)

                    if response.status_code == 200:
                        return Response({'message': 'Data sent successfully'}, status=status.HTTP_201_CREATED)
                    else:
                        return Response({'message': 'Failed to send data'},
                                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'Not found in FNS API'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer


# class UserList(generics.ListAPIView):
#     queryset = Users.objects.all()
#     serializer_class = UserSerializer


# Create your views here.
# def get_company(request):
#     if request.method == 'POST':
#         INN = request.POST.get('INN')
#         url = 'https://api-fns.ru/api/egr'
#         params = {
#             'req': INN,
#             'key': '90bc98530dabe4d2d36c8082223e8efc56382a1f'
#         }
#
#         response = requests.get(url, params=params)
#
#         data = response.json()
#         if response.status_code == 200:
#             data = response.json()
#             value = data["items"][0]["ЮЛ"]["Руководитель"]
#             return value
#         else:
#             return None

#
# def main(request):
#     return render(request, 'main.html')
