import os
import sys
import json
import requests
from .cli import CLI
from datetime import datetime

class GraymetaClient():

    def __init__(self, server_url, api_key):
        self.SERVER_URL = server_url
        self.API_KEY = api_key
        self.HEADERS = { "Authorization": "Bearer " + self.API_KEY }
        self.verbose = False

    def summary_platform(self):
        return self.http_get("/api/data/summary/platform")

    def summary_data(self):
        return self.http_get("/api/data/summary/data")

    def extract_all(self, cli):
        """
        Extracts all item metadata to disk
        """

        # cache file file is the set of items already downloaded *not* to download again
        cache_filename = cli.getOrDie("-cache_file")
        if os.path.isfile(cache_filename):
            cache = json.loads(open(cache_filename, 'r').read())
        else:
            cache = []

        # a little cache so I don't have to re-extract
        output_dir = cli.getOrDie("-output_dir")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # search file is a results of a previous search call so we don't
        # have to call search again.  Use if present.
        if cli.containsKey("-search_file"):
            print("Not calling search, using file")
            search_filename = cli.getOrDie("-search_file")
            search_response = json.loads(open(search_filename, 'r').read())
            print("Loaded search file ok.")
        else:
            print("Calling search")
            search_response = self.search()
            print("Called search, now extracting results")


        total_results = len(search_response["results"])
        print("Retrieved " + str(total_results) + " results.")
        for r in search_response["results"]:
            start_time = datetime.today()
            result = r["result"]
            stow_url = result["stow_url"]
            filename = stow_url.split("/")[-1]
            execution_id = stow_url.split("/")[-3] + "/" + stow_url.split("/")[-2]
            gm_item_id = result["_id"]
            if gm_item_id in cache:
                print("Already processed " + gm_item_id + ", not extracting again.")
                continue

            if not os.path.exists(output_dir + "/" + execution_id):
                os.makedirs(output_dir + "/" + execution_id)

            if "name" in result:
                # then it has been harvested
                gm_item = self.get_gm_item(gm_item_id)
                gm_item_v2 = self.get_gm_item_v2(gm_item_id)

                f1 = open(output_dir + "/" + execution_id + "/" + filename + "_v1.json", "w")
                f1.write(json.dumps(gm_item, indent=4))
                f1.close()

                f2 = open(output_dir + "/" + execution_id + "/" + filename + "_v2.json", "w")
                f2.write(json.dumps(gm_item_v2, indent=4))
                f2.close()

                f3 = open(output_dir + "/" + execution_id + "/" + filename + "_index.json", "w")
                f3.write(json.dumps(result, indent=4))
                f3.close()

                cache.append(gm_item_id)

                open(cache_filename, 'w').write(json.dumps(cache, indent=4))
                ttl = (datetime.today() - start_time).seconds
                print("Processed " + gm_item_id + " in " + str(ttl) + "s.")
            else:
                print(gm_item_id + " not harvested yet.")




        print("Called search ok, now fetching content.")
        print("Extract Complete")

    def extract(self, cli):
        """
        Extracts all items whose stow_url matches a search term
        """

        search_term = cli.getOrDie("-q")
        print("Extracting all items with '" + search_term + "' in their stow_url.")

        # search file is a results of a previous search call so we don't
        # have to call search again.  Use if present.
        if cli.containsKey("-search_file"):
            print("Not calling search, using file")
            search_filename = cli.getOrDie("-search_file")
            search_response = json.loads(open(search_filename, 'r').read())
            print("Loaded search file ok.")
        else:
            print("Calling search")
            search_response = self.search()
            print("Called search, now extracting results")

        # a little cache so I don't have to re-extract
        output_dir = cli.getOrDie("-output_dir")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for r in search_response["results"]:
            start_time = datetime.today()
            result = r["result"]
            stow_url = result["stow_url"]

            should_download = stow_url.find(search_term) > -1

            filename = stow_url.split("/")[-1]
            execution_id = stow_url.split("/")[-3] + "/" + stow_url.split("/")[-2]
            gm_item_id = result["_id"]

            if not should_download:
                continue

            if not os.path.exists(output_dir + "/" + execution_id):
                os.makedirs(output_dir + "/" + execution_id)

            if "name" in result:
                # then it has been harvested
                gm_item = self.get_gm_item(gm_item_id)
                gm_item_v2 = self.get_gm_item_v2(gm_item_id)

                f1 = open(output_dir + "/" + execution_id + "/" + filename + "_v1.json", "w")
                f1.write(json.dumps(gm_item, indent=4))
                f1.close()

                f2 = open(output_dir + "/" + execution_id + "/" + filename + "_v2.json", "w")
                f2.write(json.dumps(gm_item_v2, indent=4))
                f2.close()

                f3 = open(output_dir + "/" + execution_id + "/" + filename + "_index.json", "w")
                f3.write(json.dumps(result, indent=4))
                f3.close()

                ttl = (datetime.today() - start_time).seconds
                print("Processed " + gm_item_id + " in " + str(ttl) + "s.")
            else:
                print(gm_item_id + " not harvested yet.")

        print("Extract Complete")


    def features(self):
        return self.http_get("/api/data/features")

    def add_comment(self, gm_item_id, comment):
        url = "/api/data/comments"
        data = { "target_type": "item", "target_id": gm_item_id, "body": comment }
        return self.http_post(url, data)

    def list_comments(self, gm_item_id):
        url = "/api/data/comments?target_type=item&page=0&target_id=" + gm_item_id
        return self.http_get(url)

    def delete_comment(self, gm_item_id, comment_id):
        url = "/api/data/comments/" + comment_id
        return self.http_delete(url)

    def harvest_item(self, location_id, container_id, stow_url, gm_item_id, force, extractors):
        """
        POST /api/control/harvest
        {
        	"location_id": "{location_id}",
        	"item_id": "{item_id}",
        	"force": {force}
        }
        """
        url = "/api/control/harvest"
        # data = { "location_id": location_id, "container_id": container_id, "stow_url": stow_url, "gm_item_id": gm_item_id, "force": force, "override_extractors": False}
        # data = { "location_id": location_id, "item_id": gm_item_id, "force": force, "override_extractors": False, }
        data = { "location_id": location_id, "container_id": container_id, "item_stow_url": stow_url, "force": force, "extractors": extractors }
        print("harvest_item: url=" + url + ", data=" + str(data))
        return self.http_post(url, data)

    def harvest_container(self, location_id, container_id, force=False):
        """
        POST /api/control/harvest
        {
        	"location_id": "{location_id}",
        	"container_id": "{container_id}",
        	"force": {force}
        }
        """
        url = "/api/control/harvest"
        data = { "location_id": location_id, "container_id": container_id, "force": force}
        return self.http_post(url, data)

    def create_gm_item_id_from_s3_key(self, s3_key):
        """
        The asset has not yet been walked, this assigns a gm_item_id to it without harvesting
        POST /api/control/item-id
        {"location_id":"xxxx", "container_id":"xxxxx", "item_id":"filename.txt"}

        returns

        {'gm_item_id': 'xxxx', 'stow_url': 's3://https://xxxxx/content.mp4'}

        """

        print("gmapi.create_gm_item_id_from_s3_key(" + s3_key + ")")
        key = s3_key.replace("s3://", "")
        splits = key.split("/")
        bucket = splits[0]
        filename = "/".join(splits[1:])

        locations = self.list_locations()
        location_id = locations["locations"][0]["id"]
        containers = self.list_containers(location_id)

        container = None
        for candidate_container in containers["containers"]:
            if candidate_container["id"] == bucket:
                container_id = candidate_container["id"]
                break

        url = "/api/control/item-id"
        post_data = { "location_id": location_id, "container_id": container_id, "item_id": filename }
        print(post_data)
        return self.http_post(url, post_data)

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
        return self.http_get("/api/data/items/" + gm_item_id)

    def get_gm_item_v2(self, gm_item_id):
        return self.http_get("/files/" + gm_item_id + "/metadata2.json")

    def list_items(self, container_id):
        return self.http_get("/api/data/items")

    def delete_gm_item(self, gm_item_id):
        url = self.SERVER_URL + "/api/data/items/" + gm_item_id
        headers = self.HEADERS
        r = requests.delete(url, headers=headers)
        return r.json()

    def upload_captions(self, gm_item_id, stl_filename):
        url = self.SERVER_URL + "/api/data/items/" + gm_item_id + "/captions"
        headers = self.HEADERS
        files = { "caption_file": open(stl_filename, 'rb') }
        cfg = { "verbose": sys.stderr }
        r = requests.post(url, files=files, headers=headers, config=cfg)
        return r.json()

    def get_captions(self, gm_item_id):
        url = "/api/data/items/" + gm_item_id + "?only=captions.captions"
        return self.http_get(url)

    def delete_captions(self, gm_item_id, captions_id):
        url = self.SERVER_URL + "/api/data/items/" + gm_item_id + "/captions?caption_id=" + captions_id
        headers = self.HEADERS
        r = requests.delete(url, headers=headers)
        return r.json()
  
    def list_location(self, location_id):
        return self.http_get("/api/data/locations/" + location_id)

    def list_locations(self):
        return self.http_get("/api/data/locations")

    def list_containers(self, location_id):
        return self.http_get("/api/data/locations/" + location_id + "/containers")

    def list_enabled_containers(self):
        """
        GET /api/data/containers/enabled
        """
        return self.http_get("/api/data/containers/enabled")

    def health(self):
        return self.http_get("/api/data/healthz")

    def stats(self):
        """
{
    "queue_depths": {
        "index": 0,
        "stage09": 0,
        "stage08": 0,
        "stage05": 0,
        "stage04": 0,
        "stage07": 0,
        "stage06": 0,
        "stage01": 0,
        "stage00": 0,
        "stage03": 0,
        "stage02": 0,
        "activity": 0,
        "walk": 0
    },
    "jobs": {
        "running": 0,
        "pending": 0
    }
}
        """
        return self.http_get("/api/control/system/stats")

    def activity(self):
        return self.http_get("/api/data/activity")

    def user(self):
        return self.http_get("/api/data/user")

    def platform(self):
        return self.http_get("/api/data/summary/platform")

    def scroll(self):
        return self.http_post("/api/data/scroll", {})

    def search(self, limit=50000):
        data = { "limit": limit }
        return self.http_post("/api/data/search", data)

    def search_quick(self, limit=50000):
        data = { "limit": limit, "only": [ "gm_item_id" ] }
        return self.http_post("/api/data/search", data)

    def search_extracted(self, limit=50000):
        filters = { "exists": [ { "field": "extracted", "value": True } ] }
        data = { "limit": limit, "filters": filters }
        return self.http_post("/api/data/search", data)

    def search_not_extracted(self, limit=50000):
        filters = { "not_exists": [ { "field": "extracted", "value": True } ] }
        data = { "limit": limit, "filters": filters }
        return self.http_post("/api/data/search", data)

    def search_last_modified(self, date_from, date_to, limit=1000):
        data = { "limit": limit, "last_modified": { "from": date_from, "to": date_to } }
        return self.http_post("/api/data/search", data)

    def search_last_harvested(self, date_from, date_to, limit=1000):
        data = { "limit": limit, "last_harvested": { "from": date_from, "to": date_to } }
        return self.http_post("/api/data/search", data)

    def compilations(self):
        return self.http_get("/api/data/summary/compilations")

    def keyword_list_groups(self):
        return self.http_get("/api/data/keywords")

    def keyword_get_group(self, group_id):
        return self.http_get("/api/data/keyword-groups/" + group_id)

    def keyword_create_group(self, name, color):
        data = {"name": name, "color": color }
        return self.http_post("/api/data/keyword-groups", data)

    def keyword_delete_group(self, group_id):
        url = self.SERVER_URL + "/api/data/keyword-groups/" + group_id
        headers = self.HEADERS
        r = requests.delete(url, headers=headers)
        return r.json()

    def keyword_add_to_group(self, group_id, word):
        url = "/api/data/keywords/" + group_id
        data = {"word": word}
        return self.http_post(url, data)

    def keyword_remove_from_group(self, group_id, word):
        url = self.SERVER_URL + "/api/data/keywords/" + group_id + "?word=" +word
        headers = self.HEADERS
        r = requests.delete(url, headers=headers)
        return r.json()

    def http_get(self, partial_url):
        cli = CLI(sys.argv)
        verbose = self.verbose or cli.containsKey("-v")
        url = self.SERVER_URL + partial_url
        headers = self.HEADERS
        if verbose:
            print(">>\nGET: " + url + "\nHEADERS: " + str(headers) + "\n>>")
        r = requests.get(url, headers=headers)
        if r.status_code >= 200 and r.status_code < 300:
            if verbose:
                print(r)
                print(r.text)
            return r.json()
        else:
            return None

    def http_post(self, partial_url, data):
        cli = CLI(sys.argv)
        verbose = self.verbose or cli.containsKey("-v")
        url = self.SERVER_URL + partial_url
        headers = self.HEADERS
        data_str = json.dumps(data)
        if verbose:
            print(">>\nPOST: " + url + "\nBODY: " + data_str + "\nHEADERS: " + str(headers) + "\n>>")
        r = requests.post(url, data=data_str, headers=headers)
        if verbose:
            print(r)
        return r.json()

    def http_delete(self, partial_url, data=None):
        cli = CLI(sys.argv)
        verbose = self.verbose or cli.containsKey("-v")
        url = self.SERVER_URL + partial_url
        headers = self.HEADERS
        if data:
            data_str = json.dumps(data)
        else:
            data_str = ""

        if verbose:
            print(">>\nDELETE: " + url + "\nBODY: " + data_str + "\nHEADERS: " + str(headers) + "\n>>")
        r = requests.delete(url, data=data_str, headers=headers)
        if verbose:
            print(r)
        return r.json()



