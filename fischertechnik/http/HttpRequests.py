import requests
import json


class HttpRequests:

    @staticmethod
    def __http_request(url, headers, data, method):
        try:
            # The required format is: {"Header1": "Header1"}.
            # The input value of headers is expected as string,
            # the json.load operation removes the first quotation marks.
            _headers = json.loads(headers)
            _data = data
            # Timeout-Tuple = (connect, read)
            _timeout = (3, 20)

            if method == "get":
                r = requests.get(url, headers=_headers, timeout=_timeout)
            elif method == "post":
                r = requests.post(url, headers=_headers, data=_data, timeout=_timeout)
            elif method == "put":
                r = requests.put(url, headers=_headers, data=_data, timeout=_timeout)
            elif method == "patch":
                r = requests.patch(url, data=_data, headers=_headers, timeout=_timeout)
            elif method == "delete":
                r = requests.delete(url, headers=_headers, data=_data, timeout=_timeout)
            else:
                raise ValueError("Illegal Argument: Unknown HTTP-Method")

            if r.status_code == 200:
                return json.dumps(r.json())
            else:
                return json.dumps(r.status_code)

        except Exception as exc:
            raise ValueError("Something went wrong, please check your input values!") from exc

    @staticmethod
    def get_request(url, headers):
        try:
            return HttpRequests.__http_request(url, headers, None, "get")
        except ValueError as ve:
            return ve

    @staticmethod
    def post_request(url, headers, data):
        try:
            return HttpRequests.__http_request(url, headers, data, "post")
        except ValueError as ve:
            return ve

    @staticmethod
    def put_request(url, headers, data):
        try:
            return HttpRequests.__http_request(url, headers, data, "put")
        except ValueError as ve:
            return ve

    @staticmethod
    def patch_request(url, header, data):
        try:
            return HttpRequests.__http_request(url, header, data, "patch")
        except ValueError as ve:
            return ve

    @staticmethod
    def delete_request(url, header, data):
        try:
            return HttpRequests.__http_request(url, header, data, "delete")
        except ValueError as ve:
            return ve

