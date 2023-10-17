from utils.utils import AppUtils
from flask import request
from graph.graphops import GraphOps
from rest.restops import RestOps


class Service:

    @classmethod
    def index(cls):
        return AppUtils.make_response([{"index": "/"}])

    @classmethod
    def graphql(cls):
        params = request.json
        gql_query = params.get('query', None)
        # resp = {"data": []}
        try:
            resp = GraphOps.query(gql_query)
        except Exception as e:
            return AppUtils.make_response(e, 500, {"error": "Internal Error"})
        return AppUtils.make_response(resp)

    @classmethod
    def select(cls):
        """
        Sample input json: {
          "fields": ["sum(zone_id) as sum_zone_id", "sum(zone_id)/:div as half_sum_zone_id", "cloud_regions.region_name as region_name", "cloud_service_providers.provider_name"],
          "table": "zones",
          "inner": ["cloud_regions"],
          "left": ["cloud_service_providers"],
          "where": "zone_id > :zoneId and region_name like :regionName",
          "group": ["zone_id", "cloud_regions.region_name", "cloud_service_providers.provider_name"],
          "having": "sum(zone_id) > :zoneIdSum",
          "sort": ["zone_name asc"],
          "bind": {"div":2, "zoneId":0, "regionName": "%north%", "zoneIdSum": 100},
          "limit": 2,
          "offset": 1
        }
        """
        params = request.json
        try:
            # api call
            resp = RestOps.post(params, endpoint='/api/select')
        except Exception as e:
            return AppUtils.make_response(e, 500, {"error": "Internal Error"})
        return AppUtils.make_response(resp['data'], resp['code'], resp['msg'])

    @classmethod
    def add(cls):
        """
        Sample input json: {
            "table": "zones",
            "records": [{
                "zone_name": "test zone 104",
                "region_id": 41
            },{
                "zone_name": "test zone 105",
                "region_id": 41
            }]
        }
        """
        params = request.json
        try:
            # api call
            resp = RestOps.post(params, endpoint='/api/add')
        except Exception as e:
            return AppUtils.make_response(e, 500, {"error": "Internal Error"})
        return AppUtils.make_response(resp['data'], resp['code'], resp['msg'])

    @classmethod
    def edit(cls):
        """
        Sample input json: {
          "objects": [{
            "table": "zones",
            "where": "zone_id=138",
            "record":{
              "zone_name": "test zone 104",
              "region_id": 41
            }
          },{
            "table": "zones",
            "where": "zone_id=139",
            "record": {
                "zone_name": "test zone 105",
                "region_id": 41
            }
          }]
        }
        """
        params = request.json
        try:
            # api call
            resp = RestOps.post(params, endpoint='/api/update')
        except Exception as e:
            return AppUtils.make_response(e, 500, {"error": "Internal Error"})
        return AppUtils.make_response(resp['data'], resp['code'], resp['msg'])

    @classmethod
    def delete(cls):
        """
        Sample input json: {
          "objects": [{
            "table": "zones",
            "where": "zone_id=138"
          },{
            "table": "zones",
            "where": "zone_id=139"
          }]
        }
        """
        params = request.json
        try:
            # api call
            resp = RestOps.post(params, endpoint='/api/remove')
        except Exception as e:
            return AppUtils.make_response(e, 500, {"error": "Internal Error"})
        return AppUtils.make_response(resp['data'], resp['code'], resp['msg'])

    @classmethod
    def upload(cls):
        if request.method == 'POST':
            type_val = request.form.get('type', '')
            id_val = request.form.get('id', '')
            field = request.form.get('field', '')
            file = request.files['file']
            AppUtils.file_upload(type_val, id_val, field, file)
            return AppUtils.make_response([])
        else:
            return AppUtils.make_response([], 401, {"error": "File not found"})
