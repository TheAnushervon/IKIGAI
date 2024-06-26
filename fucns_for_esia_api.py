"""
--------------------------------------------------------------------------------------------------------
                CODE WAS NOT TESTED  DUE TO UNAVAILABILITY TO  ACCESS ESIA PORTAL
--------------------------------------------------------------------------------------------------------
"""

import base64
import os
import requests
from dotenv import load_dotenv
import gostcrypto

load_dotenv()

using_pycades = os.getenv("using_pycades", False)

accessTkn_esia = ""
api_key = os.getenv('apikey', 'my api key')
esia_host = os.getenv('esia_host', 'https://esia-portal1.test.gosuslugi.ru')
svcdev_host = os.getenv('svcdev_host', 'https://svcdev-beta.test.gosuslugi.ru')
private_key_path = os.getenv('private_key_path', './esia/esia/GOST 2012 PROD.cer')


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
    # Function using pycades (if installed + license key) -> generally more robust and reliable solution

    import sys
    sys.path.append(r'/usr/local/lib/pycades.so')
    import pycades

    TSAAddress = os.getenv('TSAAddress', 'http://testca2012.cryptopro.ru/tsp/tsp.srf')
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


# Example usage
if __name__ == "__main__":
    # Example to get access token
    print(get_access_token())

    # Example to create an order
    order_data = {
        # Fill with appropriate order data
    }
    print(order(order_data))

    # Example to push data
    push_data = {
        # Fill with appropriate push data
    }
    print(push(push_data))

    # Example to push chunked data
    chunked_data = {
        # Fill with appropriate chunked data
    }
    print(chunked(chunked_data))

    # Example to check status
    status_data = {
        "orderId": "example-order-id"  # Replace with actual order ID
    }
    print(status(status_data))
