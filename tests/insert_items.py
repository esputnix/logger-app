import boto3

# boto3 is the AWS SDK library for Python.
# The "resources" interface allow for a higher-level abstraction than the low-level client interface.
# More details here: http://boto3.readthedocs.io/en/latest/guide/resources.html
dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
table = dynamodb.Table('serverlessapibackend-SampleTable-XAACBDBU2LU8')


# The BatchWriteItem API allows us to write multiple items to a table in one request.
with table.batch_writer() as batch:
    # batch.put_item(Item={"deviceID": "1FMSU43F8YED08838", "err": 31982, "timestamp": 1514764801})

    # batch.put_item(Item={"deviceID": "KNDJT2A65D7536675", "err": 35201, "timestamp": 1514764802})
    # batch.put_item(Item={"id":"Logger-ID 15", "name":"Logger item 15", "deviceID": "1G11C5SL6EF215699", "err": 69472, "timestamp": 1514764800} )
    # batch.put_item(Item={"id":"id-2", "name":"name-2", "deviceID": "deviceID-2", "err": 69472, "timestamp": 1514764800} )

    # batch.put_item(Item={"name":"name-3", "deviceID": "deviceID-3", "err": 69472, "timestamp": 1514764800} )

    # batch.put_item(Item={"timestamp": 1514764800, "deviceID": "deviceID-4", "name":"name-4",  "err": 69472} )

    # batch.put_item(Item={"timestamp": 1514764800, "deviceID": "deviceID-5", "err": 69472} )


    batch.put_item(Item={"deviceID": "1FMYU03175KA63387", "err": 89011, "timestamp": 1514764808})
    batch.put_item(Item={"deviceID": "1G6KD57Y68U158520", "err": 4199, "timestamp": 1514764810})
    batch.put_item(Item={"deviceID": "JA3215H14CU015290", "err": 96616, "timestamp": 1514764812})
    batch.put_item(Item={"deviceID": "1G11C5SL6EF215699", "err": 71658, "timestamp": 1514764813})
    batch.put_item(Item={"deviceID": "1FMSU43F8YED08838", "err": 87448, "timestamp": 1514764814})
    batch.put_item(Item={"deviceID": "1N4BU31D2TC186889", "err": 41941, "timestamp": 1514764818})
    batch.put_item(Item={"deviceID": "1FAHP3M21CL495698", "err": 37664, "timestamp": 1514764819})
    batch.put_item(Item={"deviceID": "5FNRL5H69BB031000", "err": 69448, "timestamp": 1514764820})
    batch.put_item(Item={"deviceID": "KMHWF25S43A816010", "err": 65090, "timestamp": 1514764821})
    batch.put_item(Item={"deviceID": "KNDJT2A65D7536675", "err": 37474, "timestamp": 1514764822})






    # batch.put_item(Item={"deviceID": "1FMYU03175KA63387", "err": 89011})




