from requests import Response, get, post
from cocobase_client.config import BASEURL
from cocobase_client.exceptions import CocobaseError
from cocobase_client.query import QueryBuilder
from cocobase_client.record import Record
from cocobase_client.types import HttpMethod


class CocoBaseClient:
    """
    A client for interacting with the CocoBase API.
    """

    api_key = None
    token = None

    def __init__(self, api_key: str, token: str | None = None):
        self.api_key = api_key
        if token is None:
            return
        self.token = token

    def __request__(
        self, url, method: HttpMethod = HttpMethod.get, data: dict | None = None
    ) -> Response:
        if not url.startswith("/"):
            url = "/" + url

        if method not in (HttpMethod.get, HttpMethod.post):
            raise ValueError(
                "Invalid HTTP method. Use HttpMethod.get or HttpMethod.post."
            )
        url = BASEURL + url
        if method == HttpMethod.get:
            return get(url, headers={"x-api-key": self.api_key})
        else:
            return post(url, headers={"x-api-key": self.api_key}, json=data)

    def create_collection(self, collection_name, webhookurl: str | None = None):
        data = {
            "name": collection_name,
        }

        if webhookurl is not None:
            data["webhook_url"] = webhookurl

        req = self.__request__("/collections", method=HttpMethod.post, data=data)

        if req.status_code == 400:
            raise CocobaseError("Invalid Request: " + req.text)
        elif req.status_code == 422:
            raise CocobaseError("A field is missing: " + req.text)
        elif req.status_code == 500:
            raise CocobaseError("Internal Server Error")
        elif req.status_code == 201:
            return req.json()

    def update_collection(
        self,
        collection_id,
        collection_name: str | None = None,
        webhookurl: str | None = None,
    ):
        data = dict()
        if collection_id is None:
            raise CocobaseError("Collection ID must be provided.")

        if webhookurl is None and collection_name is None:
            raise CocobaseError(
                "At least one of webhook_url or collection_name must be provided."
            )

        if webhookurl is not None:
            data["webhook_url"] = webhookurl

        if collection_name is not None:
            data["name"] = collection_name

        req = self.__request__(
            f"/collections/{collection_id}", method=HttpMethod.post, data=data
        )

        if req.status_code == 400:
            raise CocobaseError("Invalid Request: " + req.text)
        elif req.status_code == 422:
            raise CocobaseError("A field is missing: " + req.text)
        elif req.status_code == 500:
            raise CocobaseError("Internal Server Error")
        elif req.status_code == 200:
            return req.json()

    def delete_collection(self, collection_id):
        if collection_id is None:
            raise CocobaseError("Collection ID must be provided.")

        req = self.__request__(f"/collections/{collection_id}", method=HttpMethod.post)

        if req.status_code == 400:
            raise CocobaseError("Invalid Request: " + req.text)
        elif req.status_code == 422:
            raise CocobaseError("A field is missing: " + req.text)
        elif req.status_code == 500:
            raise CocobaseError("Internal Server Error")
        elif req.status_code == 204:
            return True

    def create_document(self, collection_id, data: dict) -> Record | None:
        if collection_id is None:
            raise CocobaseError("Collection ID must be provided.")

        if not isinstance(data, dict):
            raise CocobaseError("Data must be a dictionary.")

        req = self.__request__(
            f"/collections/documents?collection=" + collection_id,
            method=HttpMethod.post,
            data={"data": data},
        )

        if req.status_code == 400:
            raise CocobaseError("Invalid Request: " + req.text)
        elif req.status_code == 422:
            raise CocobaseError("A field is missing: " + req.text)
        elif req.status_code == 500:
            raise CocobaseError("Internal Server Error")
        elif req.status_code == 201:
            return Record(req.json())

    def list_documents(
        self, collection_id, query: QueryBuilder | None = None
    ) -> list[Record] | None:
        url = None
        if collection_id is None:
            raise CocobaseError("Collection ID must be provided.")
        if query is not None and not isinstance(query, QueryBuilder):
            raise CocobaseError("Query must be an instance of QueryBuilder.")
        if query is not None:
            url = f"/collections/{collection_id}/documents?{query.build()}"
        else:
            url = f"/collections/{collection_id}/documents"
        req = self.__request__(url)

        if req.status_code == 400:
            raise CocobaseError("Invalid Request: " + req.text)
        elif req.status_code == 422:
            raise CocobaseError("A field is missing: " + req.text)
        elif req.status_code == 500:
            raise CocobaseError("Internal Server Error")
        elif req.status_code == 200:
            return [Record(doc) for doc in req.json()]

    def get_document(self, collection_id, document_id) -> Record | None:
        if collection_id is None:
            raise CocobaseError("Collection ID must be provided.")
        if document_id is None:
            raise CocobaseError("Document ID must be provided.")

        req = self.__request__(f"/collections/{collection_id}/documents/{document_id}")

        if req.status_code == 400:
            raise CocobaseError("Invalid Request: " + req.text)
        elif req.status_code == 422:
            raise CocobaseError("A field is missing: " + req.text)
        elif req.status_code == 500:
            raise CocobaseError("Internal Server Error")
        elif req.status_code == 200:
            return Record(req.json())

    def delete_document(self, collection_id, document_id) -> bool:
        if collection_id is None:
            raise CocobaseError("Collection ID must be provided.")
        if document_id is None:
            raise CocobaseError("Document ID must be provided.")

        req = self.__request__(
            f"/collections/{collection_id}/documents/{document_id}",
            method=HttpMethod.delete,
        )

        if req.status_code == 400:
            raise CocobaseError("Invalid Request: " + req.text)
        elif req.status_code == 422:
            raise CocobaseError("A field is missing: " + req.text)
        elif req.status_code == 500:
            raise CocobaseError("Internal Server Error")
        elif req.status_code == 200 or req.status_code == 204:
            return True
        return False

    def update_document(self, collection_id, document_id, data: dict) -> Record | None:
        if collection_id is None:
            raise CocobaseError("Collection ID must be provided.")
        if document_id is None:
            raise CocobaseError("Document ID must be provided.")
        if not isinstance(data, dict):
            raise CocobaseError("Data must be a dictionary.")

        req = self.__request__(
            f"/collections/{collection_id}/documents/{document_id}",
            method=HttpMethod.patch,
            data={"data": data},
        )

        if req.status_code == 400:
            raise CocobaseError("Invalid Request: " + req.text)
        elif req.status_code == 422:
            raise CocobaseError("A field is missing: " + req.text)
        elif req.status_code == 500:
            raise CocobaseError("Internal Server Error")
        elif req.status_code == 200:
            return Record(req.json())
