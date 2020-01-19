# Messageboard App
## Introduction
#### This is a simple messageboard backend app build using serverless framework, python3, AWS DynamoDB, AWS Lambda and AWS API Gateway. host name: `https://ttjoypag8g.execute-api.us-east-1.amazonaws.com/dev`
---
### Endpoints
#### GetUser - Returns user data that corresponsed to user_id
`GET - /users/{user_id}`
```
Response:
{
    "email": {
        "S": "sample@email.com"
    },
    "name": {
        "S": "John Doe"
    },
    "userId": {
        "S": "d2c7040d1bec3fd0971783d70b981bd4"
    }
}
```
#### GetAllUsers - Returns a list of registered users
`GET - /users`
```
Response:
[{
    "email": {
        "S": "sample@email.com"
    },
    "name": {
        "S": "John Doe"
    },
    "userId": {
        "S": "d2c7040d1bec3fd0971783d70b981bd4"
    }
}]
```
#### createUser: - Create a new user
`POST - /users`
```
payload:
{
  "name": "John Doe"
  "email": "sample@email.com"
}
Response:
{
    "email": "sample@email.com",
    "name": "John Doe",
}
```
#### getUserBoards - Get all messageboards ids where user has a post
`GET - /users/{user_id}/messageboards`
```
Response:
[{
    "board_id": {
      "S": "0d945fee8fbb46a8877d89f1fc0ea183"
    }
}]
```

#### getAllMessageboards - Retrieves all existing messageboards
`GET - /messageboards`
```
Response:
[{
  "boardname": {
    "S": "MSGBoard1"
  },
  "id": {
    "S": "09ac4add309e3902878e85fb27675dc9"
  }
}]
```
#### createMessageboard - Create a new messageboard
`POST - /messageboards`
```
payload:
{
	"boardname": "MSGBoard1"
}
response:
{
  "boardname": "MSGBoard1",
  "id": "09ac4add309e3902878e85fb27675dc9"
}
```
#### getMessages - Get all messages in a messageboard
`GET - /messageboards/{id}/messages`
```
response:
[
  {
    "board_id": {
      "S": "0d945fee8fbb46a8877d89f1fc0ea183"
    },
    "id": {
      "S": "7c5fa100da794afc8cb13685c5572877"
    },
    "message": {
      "S": "here is my message 1"
    },
    "user_id": {
      "S": "c85a6b0d15254943828dfeaca2a2ba68"
    }
  }
]
```
#### createMessage - Create a new message in a messageboard
`POST - /messageboards/{id}/messages`
```
payload:
{
  "message": "here is my message",
	"user_id": "c85a6b0d15254943828dfeaca2a2ba68"
}
response: 
{
  "id": "7c5fa100da794afc8cb13685c5572877",
  "message": "here is my message 1"
}
```



