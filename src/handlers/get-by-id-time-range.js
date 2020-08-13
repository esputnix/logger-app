const dynamodb = require('aws-sdk/clients/dynamodb');
const docClient = new dynamodb.DocumentClient();
const tableName = process.env.SAMPLE_TABLE;

exports.getByIdTimeRangeHandler = async (event) => {
  const { httpMethod, path, pathParameters, queryStringParameters } = event;
  if (httpMethod !== 'GET') {
    throw new Error(`getByIdHandler only accept GET method, you tried: ${httpMethod}`);
  }
  console.log('....received:', JSON.stringify(event));

  const { id } = pathParameters;

  // let startDate = '2017-11-05T08:15:30Z'
  // let endDate = '2021-11-05T08:15:30Z'
  
  let startDate = queryStringParameters.startDate;
  let endDate = queryStringParameters.endDate;

  let start_timestamp = new Date(startDate).getTime() / 1000
  let end_timestamp = new Date(endDate).getTime() / 1000
  
  console.log("start_timestamp:", start_timestamp)
  console.log("end_timestamp:", end_timestamp)

  console.log('....id:', id);
  console.log('....pathParameters:', pathParameters);
  
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
    TableName: tableName
  };

  console.log('....params:', params);

  let data = await docClient.query(params).promise();

  console.log('....data:', data);

  let items = [];
  for (let i = 0; i < data.Items.length; i++) {
      let item = data.Items[i];
      items.push({"deviceId": item.deviceID });
  };
  console.log('....items:', items);

  const response = {
    statusCode: 200,
    body: JSON.stringify(items),
  };

  console.log(`...response from: ${path} statusCode: ${response.statusCode} body: ${response.body}`);
  return response;
};
