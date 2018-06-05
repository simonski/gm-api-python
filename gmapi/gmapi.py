import sys
import json
import requests

class GraymetaClient():

    def __init__(self, server_url, api_key):
        self.SERVER_URL = server_url
        self.API_KEY = api_key
        self.HEADERS = { "Authorization": "Bearer " + self.API_KEY }

    def features(self):
        url = self.SERVER_URL + "/api/data/features"
        headers = self.HEADERS
        data = {}
        r = requests.get(url, headers=headers)
        return r.json()

    def harvest_item(self, location_id, gm_item_id):
        """
        POST /api/control/harvest
        {
        	"location_id": "{location_id}",
        	"item_id": "{item_id}",
        	"force": {force}
        }
        """
        url = self.SERVER_URL + "/api/control/harvest"
        headers = self.HEADERS
        data = { "location_id": location_id, "item_id": gm_item_id, "force": "true"}
        data_str = json.dumps(data)
        r = requests.post(url, data=data_str, headers=headers)
        return r.json()

    def harvest_container(self, location_id, container_id):
        """
        POST /api/control/harvest
        {
        	"location_id": "{location_id}",
        	"container_id": "{container_id}",
        	"force": {force}
        }
        """
        url = self.SERVER_URL + "/api/control/harvest"
        headers = self.HEADERS
        data = { "location_id": location_id, "container_id": container_id, "force": True }
        data_str = json.dumps(data)
        r = requests.post(url, data=data_str, headers=headers)
        return r.json()

    def get_gm_item_from_s3_key(self, s3_key):
        gm_item_id, location_id = self.get_gm_item_id_from_s3_key(s3_key)
        if gm_item_id != None:
            item_data = self.get_gm_item_id(str(location_id), str(container["id"]), str(filename))
            item = self.get_gm_item(gm_item_id)
            return item
        else:
            return None


    def get_gm_item_id_from_s3_key(self, s3_key):
        key = s3_key.replace("s3://", "")
        splits = key.split("/")
        bucket = splits[0]
        filename = splits[-1]

        locations = self.list_locations()
        location_id = locations["locations"][0]["id"]
        containers = self.list_enabled_containers()

        container = None
        for candidate_container in containers:
            if candidate_container["id"] == bucket:
                container = candidate_container
                break

        if container is None:
            print("No container found matching '" + bucket + "'")
            sys.exit(1)
        else:
            item_data = self.get_gm_item_id(str(location_id), str(container["id"]), str(filename))
            if item_data != None:
                gm_item_id = item_data["gm_item_id"]
                return gm_item_id, location_id
            else:
                print "No gm_item_id found."
                return None, None
               

    def get_gm_item_id(self, location_id, container_id, item_id):
        url = self.SERVER_URL + "/api/control/item-id"
        data = { "location_id": location_id, "container_id": container_id, "item_id": item_id }
        data_str = json.dumps(data)
        headers = self.HEADERS
        
        r = requests.post(url, data=data_str, headers=headers)
        if r.status_code >= 200 and r.status_code <= 299:
            return r.json()
        else:
            return None

    def get_gm_item(self, gm_item_id):
        url = self.SERVER_URL + "/api/data/items/" + gm_item_id
        headers = self.HEADERS
        r = requests.get(url, headers=headers)
        return r.json()

    def list_items(self, container_id):
        url = self.SERVER_URL + "/api/data/items"
        headers = self.HEADERS
        r = requests.get(url, headers=headers)
        return r.json()

    def delete_gm_item(self, gm_item_id):
        url = self.SERVER_URL + "/api/data/items/" + gm_item_id
        headers = self.HEADERS
        r = requests.delete(url, headers=headers)
        return r.json()

    def upload_stl(self, gm_item_id, stl_filename):
        url = self.SERVER_URL + "/api/data/items/" + gm_item_id + "/captions"
        headers = self.HEADERS
        files = { "caption_file": open(stl_filename, 'rb') }
        r = requests.post(url, files=files, headers=headers)
        return r.json()

    def list_location(self, location_id):
        url = self.SERVER_URL + "/api/data/locations/" + location_id
        headers = self.HEADERS
        r = requests.get(url, headers=headers)
        return r.json()

    def list_locations(self):
        url = self.SERVER_URL + "/api/data/locations"
        headers = self.HEADERS
        r = requests.get(url, headers=headers)
        return r.json()

    def list_containers(self, location_id):
        url = self.SERVER_URL + "/api/data/locations/" + location_id + "/containers"
        headers = self.HEADERS
        r = requests.get(url, headers=headers)
        return r.json()

    def list_enabled_containers(self):
        """
        GET /api/data/containers/enabled
        """
        url = self.SERVER_URL + "/api/data/containers/enabled"
        headers = self.HEADERS
        r = requests.get(url, headers=headers)
        return r.json()

    def health(self):
        url = self.SERVER_URL + "/api/data/healthz"
        headers = self.HEADERS
        r = requests.get(url, headers=headers)
        return r.json()

    def activity(self):
        url = self.SERVER_URL + "/api/data/activity"
        headers = self.HEADERS
        r = requests.get(url, headers=headers)
        return r.json()

    def user(self):
        url = self.SERVER_URL + "/api/data/user"
        headers = self.HEADERS
        r = requests.get(url, headers=headers)
        return r.json()

    def platform(self):
        url = self.SERVER_URL + "/api/data/summary/platform"
        headers = self.HEADERS
        r = requests.get(url, headers=headers)
        return r.json()

    def search(self):
        url = self.SERVER_URL + "/api/data/search"
        headers = self.HEADERS
        data = {'limit':9999}
        data_str = json.dumps(data)
        r = requests.post(url, data=data_str, headers=headers)
        return r.json()

    def compilations(self):
        url = self.SERVER_URL + "/api/data/summary/compilations"
        headers = self.HEADERS
        r = requests.get(url, headers=headers)
        return r.json()

    def get(self, partial_url):
        url = self.SERVER_URL + partial_url
        headers = self.HEADERS
        r = requests.get(url, headers=headers)
        return r.json()

