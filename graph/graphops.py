
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

from auth.auth import DBServiceOAuthToken
from configs.config import CONFIG


class GraphOps:

    # Select your transport with a defined url endpoint
    transport = AIOHTTPTransport(url=CONFIG['DB_SERVICE_URI']+'/graphql')

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=True)

    @classmethod
    def configureGQLClient(cls, headers: dict):
        if GraphOps.transport.headers is None:
            GraphOps.transport.headers = headers
        else:
            GraphOps.transport.headers.update(headers)
        # graph_schema = RestOps.get(endpoint='/schema', is_json_resp=False)
        GraphOps.client = Client(transport=GraphOps.transport, fetch_schema_from_transport=True)

    @classmethod
    def query(cls, gql_query):
        graph_query = gql(gql_query)
        token = DBServiceOAuthToken.getToken()
        GraphOps.configureGQLClient({'Authorization': 'Bearer '+token})
        # Execute the query on the transport
        result = GraphOps.client.execute(graph_query)
        return result
