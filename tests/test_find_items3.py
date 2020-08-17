import datetime 
from dateutil import parser

import boto3
from boto3.dynamodb.conditions import Key
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('logger-app-SampleTable-1KRQESO09KSGU')


def stringToTimestamp(datetime_str="2019-11-05T08:15:30Z"):
    return int(datetime.datetime.timestamp(parser.parse(datetime_str)))

def timestampToDatetime(timestamp=1514764902):
    return datetime.datetime.fromtimestamp(int(timestamp))

def find_by_timestamp(timestamp):        
    response = table.query( KeyConditionExpression=Key('timestamp').eq(timestamp) )
    print(response)

def find_by_deviceID(deviceID, timestamp):        
    # response = table.query( KeyConditionExpression=Key('deviceID').eq(deviceID) )
    # response = table.get_item(Key={'deviceID': deviceID, 'timestamp': timestamp})
    # response = table.get_item(Key={'timestamp': timestamp})

    # response = table.query( KeyConditionExpression=Key('timestamp').eq(timestamp) )
    # response = table.get_item(Key={'deviceID': deviceID, 'timestamp': timestamp})

    response = table.query( KeyConditionExpression=Key('timestamp').eq(timestamp) )

    print(response)

def find_by_expression(deviceID, timestamp):       
    response = table.query( KeyConditionExpression=Key('deviceID').eq(deviceID) & Key('timestamp').between(0, 1000) )
    print(response)

def find_by_date(startDate, endDate): 
    start_timestamp = stringToTimestamp(startDate)
    end_timestamp = stringToTimestamp(endDate)
    print(start_timestamp, end_timestamp)

    response = table.query( KeyConditionExpression=Key('deviceID') & Key('timestamp').between(0, 1000) )


def scan_items(query_range):
    scan_kwargs = {
        'FilterExpression': Key('deviceID').between(*query_range),
        'ProjectionExpression': "#dd, title, info.rating",
        'ExpressionAttributeNames': {"#dd": "deviceID"}
    }

    done = False
    start_key = None
    while not done:
        if start_key:
            scan_kwargs['ExclusiveStartKey'] = start_key
        response = table.scan(**scan_kwargs)
        print("....", response.get('Items', []))
        start_key = response.get('LastEvaluatedKey', None)
        done = start_key is None


def query_LatestLikes():
    # for each user, query last Y liked images
    
    timestamp = 1514764874
    response = table.query(
        IndexName='timestampIndex',
        KeyConditionExpression=Key('timestamp').eq(timestamp)
    )

    print(response)

    # if response.has_key('ConsumedCapacity'):
    #     t_rcu = response['ConsumedCapacity']['Table']['CapacityUnits']
    #     i_rcu = response['ConsumedCapacity']['LocalSecondaryIndexes'][LSI_NAME]['CapacityUnits']
    # else:
    #     t_rcu = 0.0
    #     i_rcu = 0.0
    # print "Query consumed [{}] RCUs on table, [{}] RCUs on Index.".format(t_rcu, i_rcu)
    # print
    # print "%15s | %15s | %24s | %10s" % ('ImageId', 'LastLikeUserId', 'LastLikeTime', 'TotalLikes')
    # for item in response['Items']:
    #     imageid = item['imageid']['S']
    #     last_like_userid = item['last_like_userid']['S']
    #     last_like_time = float(item['last_like_time']['N'])
    #     last_like_time_str = time.ctime(last_like_time)
    #     total_likes = item['total_likes']['N']
    #     print "%15s | %15s | %24s | %10s" % (imageid, last_like_userid, last_like_time_str, total_likes)

if __name__ == "__main__":
    query_LatestLikes()




# if __name__ == '__main__':
#     # find_by_timestamp(timestamp = 1514764898)
#     # find_by_deviceID(deviceID = "asd32", timestamp = "123")
#     # find_by_expression(deviceID = "1G6KD57Y68U158520", timestamp = "123")

    
#     # print(stringToTimestamp(datetime_str="2019-11-05T08:15:30Z"))
#     # print(stringToTimestamp(datetime_str="2020-11-05T08:15:30Z"))

#     # res = find_by_date(startDate = "2019-11-05T08:15:30Z", endDate="2020-11-05T08:15:30Z")
#     # print(res)
#     # print(timestampToDatetime(timestamp=1514764902))

#     query_range = (1414764819, 1614764819)
#     scan_movies(query_range)








