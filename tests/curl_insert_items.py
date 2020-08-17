# curl -d '{"deviceID": "1G6KD57Y68U158520", "err": 4199, "timestamp": 1514764810}' -H "Content-Type: application/json" -X POST https://a5lgfuj6sa.execute-api.us-east-1.amazonaws.com/Stage
# curl -d '{"deviceID": "1G6KD57Y68U158520", "err": 4199, "timestamp": 1514764810, "value": 1}' -H "Content-Type: application/json" -X POST https://a5lgfuj6sa.execute-api.us-east-1.amazonaws.com/Stage

import os, sys

from data import values

for i, value in enumerate(values):

    # value = str(value).replace("'", '"')
    # print(value) 

    value["status"]="active"

    cmd = """curl -d '%s' -H "Content-Type: application/json" -X POST https://a5lgfuj6sa.execute-api.us-east-1.amazonaws.com/Stage""" %str(value).replace("'", '"')

    if i > 2500:
      break 

    print(cmd)

    os.system(cmd)