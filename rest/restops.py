
import httpx
from auth.auth import DBServiceOAuthToken
from configs.config import CONFIG


class RestOps:

    RESTAPI_SERVER_URI = CONFIG['DB_SERVICE_URI']

    @classmethod
    def getDefAuthHeaders(cls):
        headers = {}
        token = DBServiceOAuthToken.getToken()
        headers['Authorization'] = 'Bearer ' + token
        return headers

    @classmethod
    def get(cls, headers: dict = {}, url=None, endpoint='/', is_json_resp=True):
        headers.update(RestOps.getDefAuthHeaders())
        if not url:
            url = RestOps.RESTAPI_SERVER_URI
        if endpoint:
            url = url + endpoint
        if is_json_resp:
            return httpx.get(url, headers=headers).json()
        else:
            return httpx.get(url, headers=headers).content

    @classmethod
    def post(cls, data, headers: dict = {}, url=None, endpoint='/', is_json_data=True, is_json_resp=True):
        headers.update(RestOps.getDefAuthHeaders())
        if not url:
            url = RestOps.RESTAPI_SERVER_URI
        if endpoint:
            url = url + endpoint
        if is_json_resp:
            return httpx.post(url, json=data, headers=headers).json()
        else:
            return httpx.post(url, data=data, headers=headers).content

    @classmethod
    def upload(cls, data, files, headers: dict, url=None, is_json_data=True):
        """
        You can also upload files, using HTTP multipart encoding:
        files = {'upload-file': open('report.xls', 'rb')}
        You can also explicitly set the filename and content type, by using a tuple of items for the file value
        files = {'upload-file': ('report.xls', open('report.xls', 'rb'), 'application/vnd.ms-excel')}
        {
            ...
            "files": {
                "file": "<... binary content ...>"
            },
            "form": {
                "message": "Hello, world!",
            },
            ...
        }
        """
        headers = headers.update(RestOps.getDefAuthHeaders())
        if not url:
            url = RestOps.RESTAPI_SERVER_URI
        if is_json_data:
            resp = httpx.post(url, json=data, files=files, headers=headers)
        else:
            resp = httpx.post(url, data=data, files=files, headers=headers)
        if resp.status_code != 200:
            return []
        return resp
