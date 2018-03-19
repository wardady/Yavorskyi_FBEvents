import ssl
import urllib.request, urllib.parse
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def fb_events(place):
    url_request = "https://graph.facebook.com/search?"
    app_access_token = "156602458392103|b9VEirBcdzsRCC0zAT2kWvIfBTU"
    access_token = "EAACObdnnRicBAKtfgnEWVCzv9oWQsnEgPDPFirgOCbQYHaZCoIvVYBpiT3ToQhX1jMKBhjZC2FAwDlrEeA3D0c8u8c2W9lkbtqLCWG3N0eOZCCXfOBUJvp2Vzrm9i2eNZBZBkqJHakUL9hiOQgUQyr3KXZCSAZCjFFgJhFYPuZAmfwZDZD"
    data = dict()
    data["q"] = place
    data["type"] = "event"
    data["access_token"] = access_token
    url_data = urllib.parse.urlencode(data)

    events_id_list = []
    while True:
        with urllib.request.urlopen(url_request + url_data) as response:
            fb_events = json.loads(response.read())
            for i in fb_events["data"]:
                events_id_list.append(i["id"])
            if fb_events.get("paging", None):
                data["after"] = fb_events["paging"]["cursors"]["after"]
            else:
                break
        break
    fb_url = "https://graph.facebook.com/v2.4/"
    events_dict = dict()
    events_dict['NONE'] = []
    for i in events_id_list:
        event_url = fb_url + i + "?"
        data = dict()
        data["fields"] = "name,description,category"
        data["access_token"] = app_access_token
        url_values = urllib.parse.urlencode(data)
        try:
            with urllib.request.urlopen(event_url + url_values) as response:
                fb_events_list = json.loads(response.read())
                if "category" in fb_events_list:
                    if fb_events_list["category"] in events_dict:
                        events_dict[fb_events_list["category"]] += [
                            fb_events_list["name"]]
                    else:
                        events_dict[fb_events_list["category"]] = [
                            fb_events_list["name"]]
                else:
                    if "description" in fb_events_list:
                        events_dict["NONE"] += [fb_events_list["name"]]

        except ValueError:
            pass
    return events_dict


a = fb_events('washington')
for d in a:
    print(d, ':', a[d])
