from django.shortcuts import render
import requests
import json
import base64
import gostcrypto
import os
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Users
from .serializers import UserSerializer, InputSerializer
from dotenv import load_dotenv
import sys

sys.path.append(r'/usr/local/lib/pycades.so')

load_dotenv()

using_pycades = os.getenv("using_pycades")

accessTkn_esia = ""
api_key = os.getenv('apikey')
esia_host = os.getenv('esia_host')
svcdev_host = os.getenv('svcdev_host')
private_key_path = os.getenv('private_key_path')


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

            # Using ESIA

            order_data = {
                "INN": INN,
                "MCHD": MCHD,
            }

            response = order(order_data)

            if value != "" and response.status is True:
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
                return Response({'message': 'Not found in FNS API or not authenticated with ESIA'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer


def get_access_token(api_key_input=None):
    global accessTkn_esia, api_key, esia_host
    try:
        api_key_data = api_key_input if api_key_input else api_key

        if using_pycades:
            signature = sign_key_pycades(api_key_data)
        else:
            signature = sign_key(api_key_data)

        url = f"{esia_host}/esia-rs/api/public/v1/orgs/ext-app/{api_key}/tkn?signature={signature}"
        response = requests.get(url).json()
        if "accessTkn" in response:
            accessTkn_esia = response["accessTkn"]
            api_key = api_key_data
        return response
    except Exception as err:
        return {"error": str(err)}


def sign_key(api_key):
    global private_key_path
    with open(private_key_path, 'rb') as f:
        private_key_bytes = bytearray(f.read())
        digest = gostcrypto.gosthash.new("streebog256")
        digest.update(api_key.encode())
        digest = digest.digest()

        signature = gostcrypto.gostsignature.new(gostcrypto.gostsignature.MODE_256,
                                                 gostcrypto.gostsignature.CURVES_R_1323565_1_024_2019[
                                                     'id-tc26-gost-3410-2012-256-paramSetB']).sign(
            private_key_bytes, digest)
    return base64.urlsafe_b64encode(signature).decode('utf-8')


def sign_key_pycades(api_key):
    import pycades
    # Function using pycades (if installed + license key) -> generally more robust and reliable solution

    TSAAddress = os.getenv('TSAAddress')
    store = pycades.Store()
    store.Open(pycades.CADESCOM_CONTAINER_STORE, pycades.CAPICOM_MY_STORE, pycades.CAPICOM_STORE_OPEN_MAXIMUM_ALLOWED)
    certs = store.Certificates
    assert (certs.Count != 0), "Certificates with private key not found"
    signer = pycades.Signer()
    signer.Certificate = certs.Item(1)
    signer.CheckCertificate = True
    signer.TSAAddress = TSAAddress
    signedData = pycades.SignedData()
    signedData.ContentEncoding = pycades.CADESCOM_BASE64_TO_BINARY
    message = api_key
    message_bytes = message.encode("utf-8")
    base64_message = base64.b64encode(message_bytes)
    signedData.Content = base64_message.decode("utf-8")
    bDetached = int(1)
    signature = signedData.SignCades(signer, pycades.CADESCOM_CADES_BES, bDetached)
    signature = signature.replace("\r\n", "", )
    signature = signature + "=" * (4 - len(signature) % 4)
    message_bytes = base64.b64decode(signature)
    result = (base64.urlsafe_b64encode(message_bytes)).decode("utf-8")
    return result


def make_request(endpoint, data):
    global accessTkn_esia, svcdev_host
    headers = {"Authorization": f"Bearer {accessTkn_esia}", "content-type": "application/json"}
    url = f"{svcdev_host}{endpoint}"
    response = requests.post(url, headers=headers, json=data, verify=False)
    return response.json()


def order(data):
    return make_request("/api/gusmev/order", data)


def push(data):
    return make_request("/api/gusmev/push", data)


def chunked(data):
    return make_request("/api/gusmev/push/chunked", data)


def status(data):
    order_id = data.get("orderId")
    endpoint = f"/api/gusmev/order/{order_id}?embed=STATUS_HISTORY"
    return make_request(endpoint, data)
