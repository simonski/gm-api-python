import sys
import os
import json

from gmapi import GraymetaClient

VERSION="1.0.21"
COMMAND="gm"

def usageAndDie():
    print "gm is a tool for querying a graymeta.com installation over https"
    print ""
    print "Usage: "
    print ""
    print "    gm command [arguments]"
    print ""
    server_url = os.environ.get("GRAYMETA_SERVER_URL") or None
    server_key = os.environ.get("GRAYMETA_API_KEY") or None
    ljust_value = 60

    if server_url:
        print "    GRAYMETA_SERVER_URL".ljust(ljust_value) + ": " + server_url
    else:
        print "    GRAYMETA_SERVER_URL".ljust(ljust_value) + ": unset - please `export GRAYMETA_SERVER_URL=http://your-graymeta-server`"

    if server_key:
        print "    GRAYMETA_API_KEY".ljust(ljust_value) + ": xxxxxxxx"
    else:
        print "    GRAYMETA_API_KEY".ljust(ljust_value) + ": unset - please `export GRAYMETA_API_KEY=xxxxxxx`"

    print ""
    print "The commands are:"
    print ""
    print "    list_locations".ljust(ljust_value) + "- displays all locations"
    print "    list_location {location_id}".ljust(ljust_value) + "- gets information on a specific location"
    print ""

    print "    list_containers {location_id}".ljust(ljust_value) + "- displays enabled containers"
    print "    list_all_containers {location_id}".ljust(ljust_value) + "- displays all containers"

    print "    list_items {container_id}".ljust(ljust_value) + "- displays items in a container"
    print ""
    print "    get_item_id {location_id} {container_id} {item_id}".ljust(ljust_value) + "- gets metadata for an item"
    print "    get_item_from_s3_key {s3_key}".ljust(ljust_value) + "- gets item from the s3 path"
    print "    get_item {item_id}".ljust(ljust_value) + "- gets metadata for an item"
    print ""
    print "    upload_stl {gm_item_id} {stl_filename} ".ljust(ljust_value) + "- uploads and associates an STL file with content"
    print ""

    print "    harvest_item_from_s3_key".ljust(ljust_value) + "-forces a harvest for an item via its S3 key"
    print "    harvest_item {location_id} {gm_item_id}".ljust(ljust_value) + "- forces a harvest for a specific item"
    print "    harvest_container {location_id} {container_id}".ljust(ljust_value) + "- forces a harvest for an entire container."
    print ""
    print "    version".ljust(ljust_value) + "- print current version number."
    print ""

    sys.exit(0)

def version():
    print COMMAND + " client " + VERSION + ", Compatible with Server Installation 0.21"
    
def main():

    if len(sys.argv) == 1:
        usageAndDie()

    command = sys.argv[1]
    if command == "version":
        version()
        sys.exit(1)

    server_url = os.environ.get("GRAYMETA_SERVER_URL") or None
    server_key = os.environ.get("GRAYMETA_API_KEY") or None

    if server_url  is None or server_url.strip() == "":
        print "Error, GRAYMETA_SERVER_URL is required."
        sys.exit(1)

    if server_key is None or server_key.strip() == "":
        print "Error, GRAYMETA_API_KEY is required."
        sys.exit(1)

    gm = GraymetaClient(server_url, server_key)

    if command == "get_item":
        gm_item_id = sys.argv[2]
        nicePrint(gm.get_item(gm_item_id))

    elif command == "get_item_id":
        location_id = sys.argv[2]
        container_id = sys.argv[3]
        item_id = sys.argv[4]
        nicePrint(gm.get_gm_item_id(location_id, container_id, item_id))

    elif command == "upload_stl":
        gm_item_id = sys.argv[2]
        stl_filename = sys.argv[3]
        nicePrint(gm.upload_stl(gm_item_id, stl_filename))
    
    elif command == "features":
        nicePrint(gm.features())

    elif command == "list_locations":
        nicePrint(gm.list_locations())

    elif command == "list_location":
        location_id = sys.argv[2]
        nicePrint(gm.list_location(location_id))

    elif command == "list_items":
        location_id = sys.argv[2]
        nicePrint(gm.list_items(location_id))

    elif command == "list_all_containers":
        location_id = sys.argv[2]
        nicePrint(gm.list_containers(location_id))

    elif command == "list_containers":
        nicePrint(gm.list_enabled_containers())

    elif command == "harvest_container":
        location_id = sys.argv[2]
        container_id = sys.argv[3]
        nicePrint(gm.harvest_container(location_id, container_id))

    elif command == "harvest_item":
        location_id = sys.argv[2]
        gm_item_id = sys.argv[3]
        nicePrint(gm.harvest_item(location_id, gm_item_id))

    elif command == "get_item_from_s3_key":
        s3_key = sys.argv[2]
        nicePrint(gm.get_item_from_s3_key(s3_key))


    else:
        usageAndDie()

def nicePrint(data):
    print(json.dumps(data, indent=4))
