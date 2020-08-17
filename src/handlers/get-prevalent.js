const dynamodb = require('aws-sdk/clients/dynamodb');
const docClient = new dynamodb.DocumentClient();
const tableName = process.env.SAMPLE_TABLE;

exports.getPrevalentHandler = async (event) => {
  const { queryStringParameters } = event;
  console.log('event:', JSON.stringify(event));

  let min = queryStringParameters.min;

  const params = { TableName: tableName };
  const { Items } = await docClient.scan(params).promise();

  let errors = [];
  for (let i = 0; i < Items.length; i++) {
    let item = Items[i];
    errors.push(item.err);
  }
  const map = errors.reduce((acc, e) => acc.set(e, (acc.get(e) || 0) + 1), new Map());
  let values = [...map.entries()];

  let result = [];
  for (let i = 0; i < values.length; i++) {
    let item = values[i];
    if (item[1] > min) {
      let countItem = {"err": item[0], "count": item[1]};
      result.push(countItem);
    };
  };

  const response = {
    statusCode: 200,
    body: JSON.stringify(result),
  };

  return response;
};
