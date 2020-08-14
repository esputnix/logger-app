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
** 2. Send a GET request to the endpoint to get the logs of the error codes in the reverse chronological order for any given device ID please run the `curl` command below. Please note that the URL ends with the deviceID. Replace it with another id to get different listing:
```
curl https://a5lgfuj6sa.execute-api.us-east-1.amazonaws.com/Stage/JA3215H14CU015290
```
Example output:
```
[{"error_code":15601, "timestamp":1514767287},
{"error_code":87830, "timestamp":1514767247},
{"error_code":57203, "timestamp":1514767243}]
```

** 3. Send a GET request to the endpoint to get the logs of the the most prevalent error codes (currently requires at least occurances for a given device id):
```
curl https://a5lgfuj6sa.execute-api.us-east-1.amazonaws.com/Stage/stat
```
Example output:
```
[[90525, 2], [84105, 2], [6150, 2], [73620, 2], [26499, 2], [28074, 2], [28589, 2], [45970, 2], [14999, 2]]
```
(The first number is the error code, while the second number shows how many times the error has occurred.)

** 4. Send a GET request to the endpoint to get the logs list that occured within a specific time frame for any given device ID. Please use the `curl` command below. This endpoint takes the `deviceID` as an argument along with the `startDate` and `endDate` Query String Parameters:
```
curl https://a5lgfuj6sa.execute-api.us-east-1.amazonaws.com/Stage/range/JA3215H14CU015290?startDate=2017-11-05T08:15:30Z&endDate=2021-11-05T08:15:30Z
```
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
curl -d '{"deviceID": "1G6KD57Y68U158520", "err": 4199, "timestamp": 1514764810, "value": 1}' -H "Content-Type: application/json" -X POST https://a5lgfuj6sa.execute-api.us-east-1.amazonaws.com/Stage
```
Example output:
```
{"deviceID": "1G6KD57Y68U158520", "err": 4199, "timestamp": 1514764810, "value": 1}
```
Please note, that the number and the names of the fields is supervised by the API. If there are any fields missing, mispelled or of unsupported data type the API returns an error.



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
