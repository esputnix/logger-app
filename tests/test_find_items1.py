import boto3
from boto3.dynamodb.conditions import Key
dynamodb = boto3.resource('dynamodb', region_name='us-east-1') # , endpoint_url="https://a5lgfuj6sa.execute-api.us-east-1.amazonaws.com/Stage"
table = dynamodb.Table('logger-app-SampleTable-1KRQESO09KSGU')




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
    # response = table.query( KeyConditionExpression=Key('deviceID').eq(deviceID) )
    # response = table.get_item(Key={'deviceID': deviceID, 'timestamp': timestamp})
    # response = table.get_item(Key={'timestamp': timestamp})

    # response = table.query( KeyConditionExpression=Key('timestamp').eq(timestamp) )
    # response = table.get_item(Key={'deviceID': deviceID, 'timestamp': timestamp})
    
    # response = table.query( KeyConditionExpression=Key('timestamp').eq(timestamp) )

    # response = table.query( KeyConditionExpression=Key('timestamp').eq(timestamp) & Key('deviceID').eq(deviceID) )


    # response = table.query( KeyConditionExpression=Key('timestamp').eq(timestamp) & Key('deviceID').between("a", "z") )

    # response = table.query( KeyConditionExpression=Key('timestamp').eq(timestamp) & Key('deviceID').eq(deviceID) )

    # response = table.query(
    #     ProjectionExpression="#yr, title, info.genres, info.actors[0]",
    #     ExpressionAttributeNames={"#yr": "year"},
    #     KeyConditionExpression=
    #         Key('year').eq(year) & Key('title').between(title_range[0], title_range[1])
    # )


    # response = table.query( KeyConditionExpression=Key('deviceID').eq(deviceID) )

    # response = table.query( KeyConditionExpression=Key('deviceID').eq(deviceID) & Key('timestamp').between("0", "1000000000") )

    # response = table.query( KeyConditionExpression=Key('deviceID').eq(deviceID) & Key('timestamp').eq("1514764810") )

    # response = table.query( KeyConditionExpression=Key('deviceID').eq(deviceID) & Key('timestamp').between(0, 10) )
    # response = table.query( KeyConditionExpression=Key('deviceID').eq(deviceID)  )
    # response = table.query( KeyConditionExpression=Key('deviceID').eq(deviceID) & Key('timestamp').between(0, 1000) )
    # response = table.query( KeyConditionExpression=Key('deviceID').eq(deviceID) & Key('timestamp').sort(0, 1000) )
    # 'EQ'|'NE'|'IN'|'LE'|'LT'|'GE'|'GT'|'BETWEEN'|'NOT

    # response = table.query(
    #     ProjectionExpression="#did, err",
    #     ExpressionAttributeNames={"#did": "deviceID"},
    #     KeyConditionExpression=Key('deviceID').eq(deviceID) & Key('timestamp').between(0, 1000) 
    # )
    
    response = table.query( KeyConditionExpression=Key('deviceID').eq(deviceID) & Key('timestamp').between(0, 1000) )
    print(response)


if __name__ == '__main__':
    # find_by_timestamp(timestamp = 1514764898)
    # find_by_deviceID(deviceID = "asd32", timestamp = "123")
    find_by_expression(deviceID = "1G6KD57Y68U158520", timestamp = "123")