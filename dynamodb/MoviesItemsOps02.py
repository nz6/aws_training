#https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.03.html

from pprint import pprint
import boto3
from botocore.exceptions import ClientError
import sys
from decimal import Decimal

def get_movie(title, year, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('Movies')

    try:
        response = table.get_item(Key={'year': year, 'title': title})
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response['Item']

def put_movie(title, year, plot, rating, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('Movies')
    response = table.put_item(
       Item={
            'year': year,
            'title': title,
            'info': {
                'plot': plot,
                'rating': rating
            }
        }
    )
    return response

def update_movie(title, year, rating, plot, actors, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('Movies')

    response = table.update_item(
        Key={
            'year': year,
            'title': title
        },
        UpdateExpression="set info.rating=:r, info.plot=:p, info.actors=:a",
        ExpressionAttributeValues={
            ':r': Decimal(rating),
            ':p': plot,
            ':a': actors
        },
        ReturnValues="UPDATED_NEW"
    )
    return response

def increase_rating(title, year, rating_increase, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('Movies')

    response = table.update_item(
        Key={
            'year': year,
            'title': title
        },
        UpdateExpression="set info.rating = info.rating + :val",
        ExpressionAttributeValues={
            ':val': Decimal(rating_increase)
        },
        ReturnValues="UPDATED_NEW"
    )
    return response

if __name__ == '__main__':
    if sys.argv[1] == 'put':
        movie_resp = put_movie("The Big New Movie", 2015,
                               "Nothing happens at all.", 0)
        print("Put movie succeeded:")
        pprint(movie_resp, sort_dicts=False)
    elif sys.argv[1] == 'get':
        movie = get_movie("The Big New Movie", 2015,)
        if movie:
            print("Get movie succeeded:")
            pprint(movie, sort_dicts=False)
    elif sys.argv[1] == 'update':
        update_response = update_movie(
            "The Big New Movie", 2015, 5.5, "Everything happens all at once.",
            ["Larry", "Moe", "Curly"])
        print("Update movie succeeded:")
        pprint(update_response, sort_dicts=False)
    elif sys.argv[1] == 'increase':
        update_response = increase_rating("The Big New Movie", 2015, 1)
        print("Update movie succeeded:")
        pprint(update_response, sort_dicts=False)
