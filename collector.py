#!/usr/bin/env python
import http.client
import json
from os.path import exists, getsize


def get_link():
    conn = http.client.HTTPSConnection("this-person-does-not-exist.com")
    conn.request("GET","/en?new")
    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))
    status = res.status

    return data, status


def get_image():
    response = get_link()
    file_name = "ai_generated_pictures/" + response[0]["name"][7:]
    if response[1] == 200:
        if not exists(file_name):
            conn = http.client.HTTPSConnection("this-person-does-not-exist.com")
            conn.request("GET",f"/img/{response[0]['name']}")
            res = conn.getresponse()
            data = res.read()
            if res.status == 200:
                with open(file_name,'xb') as f:
                    f.write(data)
                print('Image sucessfully Downloaded: ', file_name)
            else:
                print(f"Invalid response from get_image(). Response code: {res.status}")
        else:
            if getsize(file_name) == 0:
                conn = http.client.HTTPSConnection("this-person-does-not-exist.com")
                conn.request("GET",f"/img/{response[0]['name']}")
                res = conn.getresponse()
                data = res.read()
                conn.close()
                if res.status == 200:
                    with open(file_name,'wb') as f:
                        f.write(data)
                    print('Image sucessfully Downloaded: ', file_name)
                else:
                    print(f"File exists: {file_name}")
    else:
        print(f"Invalid response from get_link(). Response code: {response[1]}")


def main():
    get_image()


if __name__=="__main__":
    main()
