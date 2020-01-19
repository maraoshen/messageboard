import uuid
import os
import boto3
from boto3.dynamodb.conditions import Attr

from flask import Flask, jsonify, request
app = Flask(__name__)

USERS_TABLE = os.environ['USERS_TABLE']
MESSAGEBOARDS_TABLE = os.environ['MESSAGEBOARDS_TABLE']
MESSAGES_TABLE = os.environ['MESSAGES_TABLE']
IS_OFFLINE = os.environ.get('IS_OFFLINE')

if IS_OFFLINE:
    client = boto3.client(
        'dynamodb',
        region_name='localhost',
        endpoint_url='http://localhost:8000'
    )
else:
    client = boto3.client('dynamodb')


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/users/<string:user_id>")
def get_user(user_id):
    resp = client.get_item(
        TableName=USERS_TABLE,
        Key={
            'userId': { 'S': user_id }
        }
    )
    item = resp.get('Item')
    if not item:
        return jsonify({'error': 'User does not exist'}), 404

    return jsonify(item)

@app.route("/users")
def get_all_users():
    resp = client.scan(
        TableName=USERS_TABLE,
        Select='ALL_ATTRIBUTES'
    )
    items = resp.get('Items')
    if not items:
        return jsonify({'error': 'No users found'}), 404

    return jsonify(items)


@app.route("/users", methods=["POST"])
def create_user():
    email = request.json.get('email')
    name = request.json.get('name')
    if not email or not name:
        return jsonify({'error': 'Please provide email and name'}), 400

    user_id = uuid.uuid4().hex
    resp = client.put_item(
        TableName=USERS_TABLE,
        ConditionExpression='attribute_not_exists(email)',
        Item={
            'userId': {'S': user_id },
            'name': {'S': name },
            'email': {'S': email}
        }
    )

    return jsonify({
        'userId': user_id,
        'name': name
    })

@app.route("/messageboards")
def get_all_messageboards():
    resp = client.scan(
        TableName=MESSAGEBOARDS_TABLE,
        Select='ALL_ATTRIBUTES'
    )
    items = resp.get('Items')
    if not items:
        return jsonify({'error': 'No messageboards found'}), 404

    return jsonify(items)

@app.route("/messageboards", methods=["POST"])
def create_messageboard():
    boardname = request.json.get('boardname')
    if not boardname:
        return jsonify({'error': 'Please provide name for the Messageboard'}), 400

    id = uuid.uuid4().hex
    resp = client.put_item(
        TableName=MESSAGEBOARDS_TABLE,
        ConditionExpression='attribute_not_exists(boardname)',
        Item={
            'id': {'S': id },
            'boardname': {'S': boardname }
        }
    )

    return jsonify({
        'id': id,
        'boardname': boardname
    })

@app.route("/messageboards/<string:id>/messages")
def get_messages(id):
    resp = client.scan(
        TableName=MESSAGES_TABLE,
        FilterExpression="board_id = :id",
        ExpressionAttributeValues={':id': {'S': id}},
        Select='ALL_ATTRIBUTES'
    )
    items = resp.get('Items')
    if not items:
        return jsonify({'error': 'No messages found'}), 404

    return jsonify(items)

@app.route("/messageboards/<string:board_id>/messages", methods=["POST"])
def create_message(board_id):
    message = request.json.get('message')
    user_id = request.json.get('user_id')
    if not message or not user_id:
        return jsonify({'error': 'Please provide message and user_id'}), 400

    id = uuid.uuid4().hex
    resp = client.put_item(
        TableName=MESSAGES_TABLE,
        Item={
            'id': {'S': id },
            'message': {'S': message },
            'user_id': {'S': user_id },
            'board_id': {'S': board_id }
        }
    )

    return jsonify({
        'id': id,
        'message': message
    })

@app.route("/users/<string:user_id>/messageboards")
def get_user_boards(user_id):
    resp = client.scan(
        TableName=MESSAGES_TABLE,
        Select='SPECIFIC_ATTRIBUTES',
        FilterExpression="user_id = :user_id",
        ExpressionAttributeValues={':user_id': {'S': user_id}},
        ProjectionExpression='board_id'
    )
    items = resp.get('Items')
    if not items:
        return jsonify({'error': 'No messages found'}), 404

    return jsonify(items)
