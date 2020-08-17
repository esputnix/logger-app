import datetime 
from dateutil import parser
from collections import Counter
import pprint 
import boto3
from boto3.dynamodb.conditions import Key
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('logger-app-SampleTable-I92ZQMWUI63R')


def stringToTimestamp(datetime_str="2019-11-05T08:15:30Z"):
    return int(datetime.datetime.timestamp(parser.parse(datetime_str)))

def timestampToDatetime(timestamp=1514764902):
    return datetime.datetime.fromtimestamp(int(timestamp))

def find_by_timestamp(timestamp):        
    response = table.query( KeyConditionExpression=Key('timestamp').eq(timestamp) )
    print(response)

def find_by_deviceID(deviceID):        
    # response = table.query( KeyConditionExpression=Key('deviceID').eq(deviceID) )
    # response = table.get_item(Key={'deviceID': deviceID, 'timestamp': timestamp})
    # response = table.get_item(Key={'timestamp': timestamp})

    # response = table.query( KeyConditionExpression=Key('timestamp').eq(timestamp) )
    # response = table.get_item(Key={'deviceID': deviceID, 'timestamp': timestamp})

    response = table.query( KeyConditionExpression=Key('deviceID').eq(deviceID) )

    print(response)
    print(len(response['Items']))

    for item in response['Items']:
        print(item['timestamp'])

def find_by_expression(deviceID, timestamp):       
    response = table.query( KeyConditionExpression=Key('deviceID').eq(deviceID) & Key('timestamp').between(0, 1000) )
    print(response)

def find_by_date(startDate, endDate): 
    start_timestamp = stringToTimestamp(startDate)
    end_timestamp = stringToTimestamp(endDate)

    # response = table.query(IndexName='timestampIndex', KeyConditionExpression=Key('timestamp').between(0, 1514764993)  )
    # response = table.query(IndexName='timeIndex', KeyConditionExpression=Key('status').eq('active') & Key('timestamp').between(start_timestamp, end_timestamp)  )
    response = table.query(IndexName='timeIndex', KeyConditionExpression=Key('status').eq('active')  )
    return response

def find_by_date(startDate, endDate): 
    start_timestamp = stringToTimestamp(startDate)
    end_timestamp = stringToTimestamp(endDate)

    # response = table.query(IndexName='timestampIndex', KeyConditionExpression=Key('timestamp').between(0, 1514764993)  )
    # response = table.query(IndexName='timeIndex', KeyConditionExpression=Key('status').eq('active') & Key('timestamp').between(start_timestamp, end_timestamp)  )
    response = table.query(IndexName='timeIndex', KeyConditionExpression=Key('status').eq('active')  )
    return response

def getPrevalentErrors():
    response = table.query(IndexName='timeIndex', KeyConditionExpression=Key('status').eq('active') )

    deviceIDS = {each['deviceID']:None for each in response['Items']}.keys()

    errors = list()

    for deviceID in deviceIDS:
        response = table.query( KeyConditionExpression=Key('deviceID').eq(deviceID))
        for row in response['Items']:
            errors.append(int(row['err']))  

    result = {key:value for key, value in Counter(errors).items() if value>1}
    pprint.pprint(result)
    print(type(result))

if __name__ == '__main__':

    # res = find_by_date(startDate = "2019-11-05T08:15:30Z", endDate="2020-11-05T08:15:30Z")
    # print(res)

    # getPrevalentErrors()

#     # find_by_timestamp(timestamp = 1514764898)
    find_by_deviceID(deviceID = "JA3215H14CU015290")
#     # find_by_expression(deviceID = "1G6KD57Y68U158520", timestamp = "123")

    
#     # print(stringToTimestamp(datetime_str="2019-11-05T08:15:30Z"))
#     # print(stringToTimestamp(datetime_str="2020-11-05T08:15:30Z"))


#     # print(timestampToDatetime(timestamp=1514764902))

#     query_range = (1414764819, 1614764819)
#     scan_movies(query_range)


    # response = table.query(
    #     ProjectionExpression="#st, #time",
    #     ExpressionAttributeNames={"#st": "status", "#time": "timestamp"},
    #     IndexName='timeIndex',
    #     KeyConditionExpression=Key('status').eq('active')
    # )






