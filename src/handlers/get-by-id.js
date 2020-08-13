const dynamodb = require('aws-sdk/clients/dynamodb');
const docClient = new dynamodb.DocumentClient();
const tableName = process.env.SAMPLE_TABLE;

exports.getByIdHandler = async (event) => {
  const { httpMethod, path, pathParameters } = event;
  if (httpMethod !== 'GET') {
    throw new Error(`getByIdHandler only accept GET method, you tried: ${httpMethod}`);
  }
  console.log('....received:', JSON.stringify(event));

  const { id } = pathParameters;

  console.log('....id:', id);
  
  var params = {
    ExpressionAttributeValues: {
      ':s': id
     },
    KeyConditionExpression: 'deviceID = :s',
    // FilterExpression: 'contains (Subtitle, :topic)',
    TableName: tableName
  };

  let data = await docClient.query(params).promise();

  let items = [];
  for (let i = 0; i < data.Items.length; i++) {
      let item = data.Items[i];
      items.push({"error_code": item.err, "timestamp": item.timestamp });
  };

  const response = {
    statusCode: 200,
    body: JSON.stringify(items.reverse()),
  };

  console.log(`...response from: ${path} statusCode: ${response.statusCode} body: ${response.body}`);
  return response;
};
