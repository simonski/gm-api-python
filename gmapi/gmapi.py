import sys
import json
import requests

class GraymetaClient():

    def __init__(self, server_url, api_key):
        self.SERVER_URL = server_url
        self.API_KEY = api_key
        self.HEADERS = { "Authorization": "Bearer " + self.API_KEY }

    def features(self):
        return self.get("/api/data/features")

    def add_comment(self, gm_item_id, comment):
        url = "/api/data/comments"
        data = { "target_type": "item", "target_id": gm_item_id, "body": comment }
        return self.post(url, data)

    def list_comments(self, gm_item_id):
        url = "/api/data/comments?target_type=item&page=0&target_id=" + gm_item_id
        return self.get(url)

    def harvest_item(self, location_id, gm_item_id):
        """
        POST /api/control/harvest
        {
        	"location_id": "{location_id}",
        	"item_id": "{item_id}",
        	"force": {force}
        }
        """
        url = "/api/control/harvest"
        data = { "location_id": location_id, "item_id": gm_item_id, "force": True}
        return self.post(url, data)

    def harvest_container(self, location_id, container_id):
        """
        POST /api/control/harvest
        {
        	"location_id": "{location_id}",
        	"container_id": "{container_id}",
        	"force": {force}
        }
        """
        url = "/api/control/harvest"
        data = { "location_id": location_id, "container_id": container_id, "force": True }
        return self.post(url, data)

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
                print("No gm_item_id found.")
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
        return self.get("/api/data/items/" + gm_item_id)

    def get_gm_item_v2(self, gm_item_id):
        return self.get("/files/" + gm_item_id + "/metadata2.json")

    def list_items(self, container_id):
        return self.get("/api/data/items")

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
        return self.get("/api/data/locations/" + location_id)

    def list_locations(self):
        return self.get("/api/data/locations")

    def list_containers(self, location_id):
        return self.get("/api/data/locations/" + location_id + "/containers")

    def list_enabled_containers(self):
        """
        GET /api/data/containers/enabled
        """
        return self.get("/api/data/containers/enabled")

    def health(self):
        return self.get("/api/data/healthz")

    def stats(self):
        return self.get("/api/control/system/stats")

    def activity(self):
        return self.get("/api/data/activity")

    def user(self):
        return self.get("/api/data/user")

    def platform(self):
        return self.get("/api/data/summary/platform")

    def search(self):
        data = { "limit": 1000 }
        return self.post("/api/data/search", data)

    def search_last_modified(self, date_from, date_to):
        data = { "limit": 1000, "last_modified": { "from": date_from, "to": date_to } }
        return self.post("/api/data/search", data)

    def search_last_harvested(self, date_from, date_to):
        data = { "limit": 1000, "last_harvested": { "from": date_from, "to": date_to } }
        return self.post("/api/data/search", data)

    def compilations(self):
        return self.get("/api/data/summary/compilations")

    def keyword_list_groups(self):
        return self.get("/api/data/keywords")

    def keyword_get_group(self, group_id):
        return self.get("/api/data/keyword-groups/" + group_id)

    def keyword_create_group(self, name, color):
        data = {"name": name, "color": color }
        return self.post("/api/data/keyword-groups", data)

    def keyword_delete_group(self, group_id):
        url = self.SERVER_URL + "/api/data/keyword-groups/" + group_id
        headers = self.HEADERS
        r = requests.delete(url, headers=headers)
        return r.json()

    def keyword_add_to_group(self, group_id, word):
        url = "/api/data/keywords/" + group_id
        data = {"word": word}
        return self.post(url, data)

    def keyword_remove_from_group(self, group_id, word):
        url = self.SERVER_URL + "/api/data/keywords/" + group_id + "?word=" +word
        headers = self.HEADERS
        r = requests.delete(url, headers=headers)
        return r.json()

    def get(self, partial_url):
        url = self.SERVER_URL + partial_url
        headers = self.HEADERS
        print str(headers)
        r = requests.get(url, headers=headers)
        print r
        print r.text
        return r.json()

    def post(self, partial_url, data):
        url = self.SERVER_URL + partial_url
        headers = self.HEADERS
        data_str = json.dumps(data)
        r = requests.post(url, data=data_str, headers=headers)
        print(r)
        return r.json()

