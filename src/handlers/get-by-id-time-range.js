const dynamodb = require('aws-sdk/clients/dynamodb');
const docClient = new dynamodb.DocumentClient();
const tableName = process.env.SAMPLE_TABLE;

exports.getByIdTimeRangeHandler = async (event) => {
  const { pathParameters, queryStringParameters } = event;

  console.log('event:', JSON.stringify(event));

  const { id } = pathParameters;

  let startDate = queryStringParameters.startDate;
  let endDate = queryStringParameters.endDate;

  let start_timestamp = new Date(startDate).getTime() / 1000
  let end_timestamp = new Date(endDate).getTime() / 1000
    
  var params = {
    ExpressionAttributeValues: {
      ':s': id,
      ":start_yr": start_timestamp,
      ":end_yr": end_timestamp 
    },
    ExpressionAttributeNames: {
      "#time": "timestamp",
    },
    KeyConditionExpression: 'deviceID = :s and #time between :start_yr and :end_yr',
    TableName: tableName,
    ScanIndexForward: true
  };

  let data = await docClient.query(params).promise();

  const response = {
    statusCode: 200,
    body: JSON.stringify(data["Items"]),
  };

  return response;
};
