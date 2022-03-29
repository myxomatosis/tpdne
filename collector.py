#!/usr/bin/env python
import http.client
import json
from os.path import exists, getsize
import logging

# set up logging to file
logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)-8s %(message)s',
                                                                    filename='collector_tpdne.log')
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)

def get_link():
    conn = http.client.HTTPSConnection("this-person-does-not-exist.com")
    conn.request("GET","/en?new")
    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))
    status = res.status

    return data, status


def get_image(num):
    for val in range(1, num + 1):
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
                    logging.info(f'{val}\t==>Image sucessfully Downloaded: {file_name}')
                else:
                    logging.warning(f"Invalid response from get_image(). Response code: {res.status}")
            else:
                if getsize(file_name) == 0:
                    conn = http.client.HTTPSConnection("this-person-does-not-exist.com")
                    conn.request("GET",f"/img/{response[0]['name']}")
                    res = conn.getresponse()
                    data = res.read()
                    if res.status == 200:
                        with open(file_name,'wb') as f:
                            f.write(data)
                        logging.info(f'{val}\t==>Image sucessfully Downloaded: {file_name}')
                    else:
                        logging.warning(f"File exists: {file_name}")
        else:
            logging.warning(f"Invalid response from get_link(). Response code: {response[1]}")
    conn.close()


def main():
    logging.info(f"Starting New Session")
    while True:
        logging.info(f"How many images do you want?")
        val = input("How many images do you want? ")
        try:
            logging.info(f"You have chosen {val}")
            get_image(int(val))
            break
        except:
                logging.warning(f"Invalid input provided. Please choose a number.")

if __name__=="__main__":
    main()
