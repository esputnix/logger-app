const dynamodb = require('aws-sdk/clients/dynamodb');
const docClient = new dynamodb.DocumentClient();
const tableName = process.env.SAMPLE_TABLE;

exports.getByIdHandler = async (event) => {
  console.log('event:', JSON.stringify(event));

  const { path, pathParameters } = event;  
  
  const { id } = pathParameters;
  
  var params = {
    ExpressionAttributeValues: {
      ':s': id
     },
    KeyConditionExpression: 'deviceID = :s',
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

  return response;
};
