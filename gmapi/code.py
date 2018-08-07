import sys
import os
import json

# py2/3 imports fix
from .gmapi import GraymetaClient
from .cli import CLI
from .constants import *

COMMAND="gm"

def usageAndDie():
    print("gm is a tool for querying a graymeta.com installation over https")
    print("https://github.com/simonski/gm-api-python")
    print("")
    print("Usage: ")
    print("")
    print("    gm command [arguments]")
    print("")
    server_url = os.environ.get("GRAYMETA_SERVER_URL") or None
    server_key = os.environ.get("GRAYMETA_API_KEY") or None
    ljust_value = 60

    if server_url:
        print("    GRAYMETA_SERVER_URL".ljust(ljust_value) + ": " + server_url)
    else:
        print("    GRAYMETA_SERVER_URL".ljust(ljust_value) + ": unset - please `export GRAYMETA_SERVER_URL=https://your-graymeta-server`")

    if server_key:
        print("    GRAYMETA_API_KEY".ljust(ljust_value) + ": xxxxxxxx")
    else:
        print("    GRAYMETA_API_KEY".ljust(ljust_value) + ": unset - please `export GRAYMETA_API_KEY=xxxxxxx`")

    print("")
    print("The commands are:")
    print("")
    print("    list_locations".ljust(ljust_value) + "- displays all locations")
    print("    list_location {location_id}".ljust(ljust_value) + "- gets information on a specific location")
    print("")
    print("    list_containers {location_id}".ljust(ljust_value) + "- displays enabled containers")
    print("    list_all_containers {location_id}".ljust(ljust_value) + "- displays all containers")
    print("")
    print("    search -json".ljust(ljust_value) + "- displays all items (-json prints json)")
    print("           -last_modified_from|-last_modified_to")
    print("           -last_harvested_from|-last_harvested_to")
    print("")
    print("    get_gm_item_id {location_id} {container_id} {item_id}".ljust(ljust_value) + "- gets the gm_item_id for ")
    print("    get_gm_item {gm_item_id}".ljust(ljust_value) + "- gets metadata for an item using the gm_item_id")
    print("    get_gm_item_v2 {gm_item_id}".ljust(ljust_value) + "- gets metadata v2 for an item using the gm_item_id")
    print("")
    print("    create_gm_item_id_from_s3_key {s3_key}".ljust(ljust_value) + "- create gm_item_id from an s3_key")
    print("    get_gm_item_id_from_s3_key {s3_key}".ljust(ljust_value) + "- gets gm_item_id from an s3_key")
    print("    get_gm_item_from_s3_key {s3_key}".ljust(ljust_value) + "- gets metadata for an item using the s3_key")
    print("")
    print("    delete_gm_item {gm_item_id}".ljust(ljust_value) + "- deletes the metadata from graymeta")
    print("")
    print("    get_captions {gm_item_id}".ljust(ljust_value) + "- returns the captions in json")
    print("    upload_captions {gm_item_id} {stl_filename} ".ljust(ljust_value) + "- uploads and associates an STL file with content")
    print("    delete_captions {gm_item_id} {captions_id}".ljust(ljust_value) + "- deletes the captions from the item")
    print("    upload_captions_content {gm_item_id} {stl_filename} ".ljust(ljust_value) + "- uploads and associates an STL file with content")
    print("")
    print("    harvest_item_from_s3_key {s3_key} {extractors}".ljust(ljust_value) + "- forces a harvest for an item via its S3 key")
    print("    harvest_container {location_id} {container_id}".ljust(ljust_value) + "- forces a harvest for an entire container.")
    print("")
    print("    comment".ljust(ljust_value) + "- uses the Graymeta Comments API")
    print("")
    print("    keyword".ljust(ljust_value) + "- uses the Graymeta Keywords API")
    print("")
    print("    extract_all".ljust(ljust_value) + "- extracts all metadata")
    print("    extract (-q term)".ljust(ljust_value) + "- extracts all metadata where 'term' is present in the stow_url")
    print("")
    print("    stats".ljust(ljust_value) + "- print current /api/control/system/stats data.")
    print("    health".ljust(ljust_value) + "- print current /api/data/healthz data.")
    print("    activity".ljust(ljust_value) + "- print current /api/data/activity data.")
    print("    version".ljust(ljust_value) + "- print current gmapi version number.")
    print("    summary_platform".ljust(ljust_value) + "- print summary information about the platform.")
    print("    summary_data".ljust(ljust_value) + "- print summary information about the data.")
    print("    get {URL}".ljust(ljust_value) + "- returns response from a GET.")
    print("")

    sys.exit(0)

def version():
    print(COMMAND + " client " + VERSION)

def main():

    if len(sys.argv) == 1:
        usageAndDie()

    command = sys.argv[1]
    if command == "version":
        version()
        sys.exit(1)

    cli = CLI(sys.argv)
    server_url = os.environ.get("GRAYMETA_SERVER_URL") or None
    server_key = os.environ.get("GRAYMETA_API_KEY") or None

    if server_url  is None or server_url.strip() == "":
        print("Error, GRAYMETA_SERVER_URL is required.")
        sys.exit(1)

    if server_key is None or server_key.strip() == "":
        print("Error, GRAYMETA_API_KEY is required.")
        sys.exit(1)

    gm = GraymetaClient(server_url, server_key)
    if cli.containsKey("-nossl"):
        gm.SSL_VERIFY = False

    if cli.containsKey("-v") or cli.containsKey("--verbose") or cli.containsKey("-verbose"):
        gm.verbose = True

    if command == "upload_captions":
        gm_item_id = sys.argv[2]
        stl_filename = sys.argv[3]
        nicePrint(gm.upload_captions(gm_item_id, stl_filename))

    elif command == "get_captions":
        gm_item_id = sys.argv[2]
        nicePrint(gm.get_captions(gm_item_id))

    elif command == "delete_captions":
        gm_item_id = sys.argv[2]
        captions_id = sys.argv[3]
        nicePrint(gm.delete_captions(gm_item_id, captions_id))

    elif command == "disable_live_harvesting":
        gm.disable_live_harvesting()

    elif command == "extract_all":
        gm.extract_all(cli)

    elif command == "extract":
        gm.extract(cli)

    elif command == "scroll":
        nicePrint(gm.scroll())

    elif command == "features":
        nicePrint(gm.features())

    elif command == "summary_platform":
        nicePrint(gm.summary_platform())

    elif command == "summary_data":
        nicePrint(gm.summary_data())

    elif command == "comment":
        cli = CLI(sys.argv)
        command = cli.getOrDefault("comment", "list")
        gm_item_id = cli.getOrDie("-gm_item_id")

        if command == "add":
            comment = cli.getOrDie("-m")
            nicePrint(gm.add_comment(gm_item_id, comment))
        elif command == "list":
            nicePrint(gm.list_comments(gm_item_id))
        elif command == "delete":
            comment_id = cli.getOrDie("-comment_id")
            nicePrint(gm.delete_comment(gm_item_id, comment_id))
            nicePrint(gm.list_comments(gm_item_id))
        else:
            print("invalid comment command - try 'add, list, delete'")

    elif command == "keyword":
        cli = CLI(sys.argv)
        command = cli.getOrDie("keyword")
        if command == "list":
            nicePrint(gm.keyword_list_groups())
        elif command == "get":
            group_id = cli.getOrDie("-group_id")
            nicePrint(gm.keyword_get_group(group_id))

        elif command == "create_group":
            name = cli.getOrDie("-name")
            color = "#" + cli.getOrDie("-color")
            nicePrint(gm.keyword_create_group(name, color))
        elif command == "delete_group":
            group_id = cli.getOrDie("-group_id")
            nicePrint(gm.keyword_delete_group(group_id))
        elif command == "add_to_group":
            group_id = cli.getOrDie("-group_id")
            word = cli.getOrDie("-word")
            nicePrint(gm.keyword_add_to_group(group_id, word))
        elif command == "remove_from_group":
            group_id = cli.getOrDie("-group_id")
            word = cli.getOrDie("-word")
            nicePrint(gm.keyword_remove_from_group(group_id, word))
        else:
            print("gm keyword (list | get | create_group | delete_group | add_to_group | remove_from_group)")

    elif command == "list_locations":
        nicePrint(gm.list_locations())

    elif command == "list_location":
        location_id = sys.argv[2]
        nicePrint(gm.list_location(location_id))

    elif command == "list_all_containers":
        location_id = sys.argv[2]
        nicePrint(gm.list_containers(location_id))

    elif command == "list_containers":
        nicePrint(gm.list_enabled_containers())

    elif command == "harvest_container":
        location_id = sys.argv[2]
        container_id = sys.argv[3]
        nicePrint(gm.harvest_container(location_id, container_id))

    elif command == "harvest_item_from_s3_key":
        s3_key = sys.argv[2]
        extractors = sys.argv[3].split(",")
        response = gm.create_gm_item_id_from_s3_key(s3_key)
        nicePrint(response)
        #gm_item_id, location_id = gm.get_gm_item_id_from_s3_key(s3_key)
        #nicePrint(gm.harvest_item(location_id, gm_item_id))

        """
        elif command == "harvest_item":
            location_id = sys.argv[2]
            gm_item_id = sys.argv[3]
            nicePrint(gm.harvest_item(location_id, gm_item_id))
        """

    elif command == "create_gm_item_id_from_s3_key":
        s3_key = sys.argv[2]
        nicePrint(gm.create_gm_item_id_from_s3_key(s3_key))

    elif command == "get_gm_item_id_from_s3_key":
        s3_key = sys.argv[2]
        gm_item_id = gm.get_gm_item_id_from_s3_key(s3_key)
        print(gm_item_id)

    elif command == "get_gm_item_id":
        location_id = sys.argv[2]
        container_id = sys.argv[3]
        item_id = sys.argv[4]
        nicePrint(gm.get_gm_item_id(location_id, container_id, item_id))

    elif command == "get_gm_item_from_s3_key":
        s3_key = sys.argv[2]
        nicePrint(gm.get_gm_item_from_s3_key(s3_key))

    elif command == "get_gm_item":
        gm_item_id = sys.argv[2]
        nicePrint(gm.get_gm_item(gm_item_id))

    elif command == "get_gm_item_v2":
        gm_item_id = sys.argv[2]
        nicePrint(gm.get_gm_item_v2(gm_item_id))

    elif command == "delete_gm_item":
        gm_item_id = sys.argv[2]
        nicePrint(gm.delete_gm_item(gm_item_id))

    elif command == "health":
        nicePrint(gm.health())

    elif command == "stats":
        nicePrint(gm.stats())

    elif command == "activity":
        nicePrint(gm.activity())

    elif command == "user":
        nicePrint(gm.user())

    elif command == "platform":
        nicePrint(gm.platform())

    elif command == "compilations":
        nicePrint(gm.compilations())

    elif command == "search_quick":
        results = gm.search_quick()
        nicePrint(results)

    elif command == "search_extracted":
        results = gm.search_extracted()

    elif command == "search_not_extracted":
        results = gm.search_not_extracted()

    elif command == "search":

        results = None
        if cli.containsKey("-last_modified_from") or cli.containsKey("-last_modified_to"):
            last_modified_from = cli.getOrDie("-last_modified_from")
            last_modified_to = cli.getOrDie("-last_modified_to")
            results = gm.search_last_modified(last_modified_from, last_modified_to)
        elif cli.containsKey("-last_harvested_from") or cli.containsKey("-last_harvested_to"):
            last_harvested_from = cli.getOrDie("-last_harvested_from")
            last_harvested_to = cli.getOrDie("-last_harvested_to")
            results = gm.search_last_harvested(last_harvested_from, last_harvested_to)
        else:
            results = gm.search()

        if cli.containsKey("-json"):
            nicePrint(results)
        else:
            if not "results" in results:
                print("No results found.")
                print(results)
            else:
                print("ItemID".ljust(35)+"Last Harvested".ljust(27) + "Last Modified".ljust(27) + "Name".ljust(20))
                for entry in results["results"]:
                    result = entry["result"]
                    gm_item_id = result["_id"]
                    container = result.get("stow_container_id") or "stow_container_id"
                    name = result.get("name") or None
                    last_modified = result.get("last_modified") or "no last modified."
                    last_harvested = result.get("last_harvested") or "no last harvested."

                    if name is not None:
                        full_name = container + "/" + name
                    else:
                        full_name = "<not harvested> ( " + result.get("stow_url") + " )"

                    print(gm_item_id.ljust(35) + last_harvested.ljust(27) + last_modified.ljust(27) + full_name.ljust(20))

    elif command == "get":
        """
        performs an authenticated GET to the API
        """
        partial_url = sys.argv[2]
        nicePrint(gm.http_get(partial_url))

    else:
        print("I don't know how to '" + command + "'")
        sys.exit(1)

def nicePrint(data):
    if data:
        print(json.dumps(data, indent=4))
    else:
        print("No data found.")
