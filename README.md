# Logger-App

## A quick test of Logger-App REST API

** 1. Send a GET request to the endpoint to get a complete list of all the log entities stored in the DynamoDB please run the `curl` command below:
```
https://a5lgfuj6sa.execute-api.us-east-1.amazonaws.com/Stage
```
Example output:
```
{"deviceID": "1N4BU31D2TC186889", "err": 98910, "timestamp":1514766730},
{"deviceID": "1N4BU31D2TC186889", "err": 75698, "timestamp":1514766731},
{"deviceID": "1N4BU31D2TC186889", "err": 35294, "timestamp":1514766784}
```
** 2. Send a GET request to the endpoint to get the logs of the error codes in the reverse chronological order for any given device ID please run the `curl` command below. Plase customize the URL with another deviceID, start and end time to get different log listing:
```
curl -X GET \
  https://a5lgfuj6sa.execute-api.us-east-1.amazonaws.com/Stage/JA3215H14CU015290 \
  -H 'Content-Type: application/javascript' \
  -H 'Postman-Token: 5023ff60-47a5-4b7f-9dea-612138fb1ea4' \
  -H 'cache-control: no-cache'
```
Example output:
```
[
    {
        "deviceId": "JA3215H14CU015290"
    },
    {
        "deviceId": "JA3215H14CU015290"
    },
    {
        "deviceId": "JA3215H14CU015290"
    },
    {
        "deviceId": "JA3215H14CU015290"
    },
    {
        "deviceId": "JA3215H14CU015290"
    }
]
```

** 3. Send a GET request to the endpoint to get the logs of the the most prevalent error codes (currently requires at least occurances for a given device id):
```
curl -X GET \
  'https://a5lgfuj6sa.execute-api.us-east-1.amazonaws.com/Stage/stat?min=1' \
  -H 'Content-Type: application/json' \
  -H 'Postman-Token: f5cd736d-f5d0-4ea9-9ff3-9a89a2048820' \
  -H 'cache-control: no-cache'
```
Example output:
```
{
    "errorsCount": [
        {
            "err": 3.1415,
            "count": 3.1415
        },
        {
            "err": 3.1415,
            "count": 3.1415
        },
        {
            "err": 3.1415,
            "count": 3.1415
        }
    ]
}

```
** 4. Send a GET request to the endpoint to get the logs list that occured within a specific time frame for any given device ID. Please use the `curl` command below. This endpoint takes the `deviceID` as an argument along with the `startDate` and `endDate` Query String Parameters:
```
curl -X GET \
  'https://a5lgfuj6sa.execute-api.us-east-1.amazonaws.com/Stage/range/JA3215H14CU015290?startDate=2017-12-05T08:15:30Z&endDate=2018-01-05T08:15:30Z' \
  -H 'Content-Type: application/javascript' \
  -H 'Postman-Token: a240a211-9b99-4fa4-81a2-234aeb2c4120' \
  -H 'cache-control: no-cache'  ```
Example output:
```
    {
        "deviceId": "JA3215H14CU015290"
    },
    {
        "deviceId": "JA3215H14CU015290"
    },
    {
        "deviceId": "JA3215H14CU015290"
    },
    {
        "deviceId": "JA3215H14CU015290"
    }

```

** 5. Send a POST request to the endpoint to publish a new error log please use the `curl` command below:
```
curl -X POST \
  https://a5lgfuj6sa.execute-api.us-east-1.amazonaws.com/Stage \
  -H 'Content-Type: application/json' \
  -H 'Postman-Token: f4e27ac2-43d2-479b-b37a-73efedf908a9' \
  -H 'cache-control: no-cache' \
  -d '{"deviceID": "9N4BU31D2TC186896", "err": 35294, "timestamp":1514766784}'
```
Example output:
```
{
    "deviceID": "9N4BU31D2TC186896",
    "timestamp": 1514766784,
    "err": 35294
}
```

# Logger-App Architecture

Logger-App is an integrated continuous delivery pipeline application. Every change pushed to the source control repository triggers a pipeline that builds and deploys this application automatically. It is made of the following resources:

**Application** – orchestrates five Node.js serverless Lambda functions, build using the AWS Serverless Application Model template.

**Pipeline** – An AWS CodePipeline pipeline that connects the other resources to enable continuous delivery.

**Repository** – A Git AWS CodeCommit repository. With every code commit, the pipeline copies the source code into an Amazon S3 bucket and passes it to the build project.

**Trigger** – An Amazon CloudWatch Events rule that watches the master branch of the repository and triggers the pipeline.

**Build project** – An AWS CodeBuild build that gets the source code from the pipeline and packages the application. The source includes a build specification with commands that install dependencies and prepare the application template for deployment.

**Deployment configuration** – The pipeline's deployment stage defines a set of actions that take the processed AWS SAM template from the build output, and deploy the new version with AWS CloudFormation.

**Bucket** – An Amazon Simple Storage Service S3 bucket for deployment artifact storage.

**Various Roles** – The pipeline's source, build, and deploy stages have IAM roles that manage AWS resources. The application's function has an execution role that allows it to upload logs and can be extended to access other services.

# System Breakdown

** 1. The Application defenition
The Logger-App application and its pipeline resources are all defined in AWS CloudFormation tempale that can be customized and extended. The application repository includes a `template.yml` template that is used to add Amazon DynamoDB tables, an Amazon API Gateway API, and other application resources. The continuous delivery pipeline is defined in a separate template outside of source control and has its own stack.

To access the Logger App using AWS console please use the link below:
```
https://console.aws.amazon.com/lambda/home?region=us-east-1#/applications
```

** 2. DynomoDB database

The DynamoDB is a fully managed NoSQL database that provides fast and predictable performance with seamless scalability. It offloads the administrative burdens of operating and scaling a distributed database, encryption at rest, provides the on-demand backup capability and automatically spreads the data and traffic for the tables. The Logger-App temlate defines a table of type `AWS::DynamoDB::Table` with the `Primary KeySchema` indexing the `deviceID` field as `hash` keytype and `timestamp` field as `range`. In additon to the `Primary KeySchema` there is a `LocalSecondaryIndexes` defined with `deviceID` as `hash` keytype and `err` as `RANGE`:
```
  SampleTable:
    Type: AWS::DynamoDB::Table
    Properties:
      AttributeDefinitions:
      - AttributeName: timestamp
        AttributeType: N
      - AttributeName: deviceID
        AttributeType: S
      - AttributeName: err 
        AttributeType: N
      - AttributeName: status 
        AttributeType: S        
      KeySchema:
      - AttributeName: deviceID
        KeyType: HASH
      - AttributeName: timestamp
        KeyType: RANGE
      ProvisionedThroughput:
        ReadCapacityUnits: !Ref 'ReadCapacityUnits'
        WriteCapacityUnits: !Ref 'WriteCapacityUnits'
      LocalSecondaryIndexes:
      - IndexName: errIndex
        KeySchema:
        - AttributeName: deviceID
          KeyType: HASH
        - AttributeName: err
          KeyType: RANGE
        Projection:
          ProjectionType: KEYS_ONLY
      GlobalSecondaryIndexes:
      - IndexName: timeIndex
        KeySchema:
        - AttributeName: status
          KeyType: HASH
        - AttributeName: timestamp
          KeyType: RANGE
        Projection:
          ProjectionType: KEYS_ONLY
        ProvisionedThroughput:
          ReadCapacityUnits: !Ref 'ReadCapacityUnits'
          WriteCapacityUnits: !Ref 'WriteCapacityUnits'
```
To access this DynamoDB table using AWS console please use the link below:
```
https://console.aws.amazon.com/dynamodb/home?region=us-east-1#tables:selected=logger-app-SampleTable-I92ZQMWUI63R;tab=items
```


** 3. CodeCommit source code repository

The CodeCommit is used here to host a `Logger-app` Git repository. The commits made to its `master` branch emit the events that trigger the CloudFormation stack that deploys the pipeline infrastructure.

To access this DynamoDB table using AWS console please use the link below:
```
https://console.aws.amazon.com/codesuite/codecommit/repositories/logger-app/browse?region=us-east-1
```

** 4. Lambda functions

While all five Lambda functions are defined in the same `template.yml` file their source code is stores in the separate `javascript` files located in the `/src/handlers/` repository folder: 
```
get-all-items.js
get-by-id-time-range.js
get-by-id.js
get-prevalent.js
put-item.js
```
```
https://console.aws.amazon.com/codesuite/codecommit/repositories/logger-app/browse/refs/heads/master/--/src/handlers?region=us-east-1
```
To grant the Lamda functions an access to the DynamoDB tables their permissions boundary has been defined as:  

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "StackResources",
      "Effect": "Allow",
      "Action": [
        "*"
      ],
      "Resource": [
        "arn:aws:dynamodb:us-east-1:644982427275:table/logger-app-SampleTable-I92ZQMWUI63R",
        "arn:aws:dynamodb:us-east-1:644982427275:table/logger-app-SampleTable-I92ZQMWUI63R/*",
        "arn:aws:apigateway:us-east-1::/restapis/a5lgfuj6sa",
        "arn:aws:apigateway:us-east-1::/restapis/a5lgfuj6sa/*",
        "arn:aws:execute-api:us-east-1:644982427275:a5lgfuj6sa",
        "arn:aws:execute-api:us-east-1:644982427275:a5lgfuj6sa/*",
        "arn:aws:lambda:us-east-1:644982427275:function:logger-app-getAllItemsFunction-HL5TRWK9ZPRW",
        "arn:aws:lambda:us-east-1:644982427275:function:logger-app-getByIdFunction-FAQWAQ4PHQPH",
        "arn:aws:lambda:us-east-1:644982427275:function:logger-app-getByIdTimeRangeFunction-1OV2IAR1SPCXS",
        "arn:aws:lambda:us-east-1:644982427275:function:logger-app-getPrevalentErrorsFunction-U88UBT1MQ0HJ",
        "arn:aws:lambda:us-east-1:644982427275:function:logger-app-putItemFunction-TCUNN2KVS1HP"
      ]
    },
    {
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:DescribeLogGroups",
        "logs:PutLogEvents",
        "xray:Put*"
      ],
      "Resource": "*",
      "Effect": "Allow",
      "Sid": "StaticPermissions"
    },
    {
      "Condition": {
        "StringEquals": {
          "aws:RequestTag/aws:cloudformation:stack-name": [
            "logger-app"
          ]
        },
        "ForAllValues:StringEquals": {
          "aws:TagKeys": "aws:cloudformation:stack-name"
        }
      },
      "Action": "*",
      "Resource": "*",
      "Effect": "Allow",
      "Sid": "StackResourcesTagging"
    }
  ]
}
```
To edit this PermissionBoundary please use the link below:
```
https://console.aws.amazon.com/iam/home?region=us-east-1#/policies/arn:aws:iam::644982427275:policy/logger-app-us-east-1-PermissionsBoundary$edit?step=edit
```
** 5. API Gateway

API Gateway acts here as the front door for the Logger-App application and is used to access data, business logic, or functionality from the backend service running as Lambda functions. It handles all the tasks involved in accepting and processing up to hundreds of thousands of concurrent API calls, including traffic management, CORS support, authorization and access control, throttling, monitoring, and API version management. 

To access the API resources please use the link below:
```
https://console.aws.amazon.com/apigateway/home?region=us-east-1#/apis/a5lgfuj6sa/resources/x9bdqbzvs1
```

For each API Resource there were four methods created: `Method Request`, `Integration Request`,  `Method Response` and `Integration Response`.
The are used to configure the Authorization, Validators, URL Query String Parameters and HTTP Request Body/Headers validation. The `AWS_IAM` along with Congito is used here for the Authorization mechanism. To access the Authorizer configuration page please use the link below:
```
https://console.aws.amazon.com/apigateway/home?region=us-east-1#/apis/a5lgfuj6sa/authorizers
```
** 6. Congito and Authorization tokens

To secure the API calls there are several methods available. To complete the token authentication mechanism implemented in the Logger-App API Gateway
there was a Congitor User Pool defined with the `App client settings` configured to Allow OAuth Flows with `Implicit grant` option. It offers a single step authorization tokens generation. The second `Authorization code grant` option available as well. It can be used to secure the token generation with a two steps process. With the Authorization enabled, the API Gateway will be expecting the authorization token supplied with the `Authorizer` header. To access the `API-AUTH-USERS-POOl` please use the link below:
```
https://console.aws.amazon.com/cognito/users/?region=us-east-1#/pool/us-east-1_mPgGZlgTd/app-integration-app-settings?_k=111q83
```


