import boto3
from boto3.dynamodb.conditions import Key
dynamodb = boto3.resource('dynamodb', region_name='us-east-1') # , endpoint_url="https://a5lgfuj6sa.execute-api.us-east-1.amazonaws.com/Stage"

from decimal import Decimal
import json

def load_movies(movies):
    table = dynamodb.Table('Movies')
    for movie in movies:
        year = int(movie['year'])
        title = movie['title']
        print("Adding movie:", year, title)
        table.put_item(Item=movie)


if __name__ == '__main__':
    with open("/Users/c-pasha.ivanov/gits/esputnix/aws/lambdas/logger-app/tests/moviedata.json") as json_file:
        movie_list = json.load(json_file, parse_float=Decimal)
    load_movies(movie_list)


import boto3
from boto3.dynamodb.conditions import Key
dynamodb = boto3.resource('dynamodb', region_name='us-east-1') # , endpoint_url="https://a5lgfuj6sa.execute-api.us-east-1.amazonaws.com/Stage"


def get_movie(title, year, dynamodb=None):
    table = dynamodb.Table('Movies')

    try:
        response = table.get_item(Key={'year': year, 'title': title})
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response['Item']


if __name__ == '__main__':
    movie = get_movie("The Big New Movie", 2015,)
    if movie:
        print("Get movie succeeded:")
        pprint(movie, sort_dicts=False)