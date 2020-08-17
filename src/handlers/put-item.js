const dynamodb = require('aws-sdk/clients/dynamodb');

const docClient = new dynamodb.DocumentClient();
const tableName = process.env.SAMPLE_TABLE;

exports.putItemHandler = async (log) => {
  console.log('log:', log);

  let deviceID = log.deviceID;
  let err = log.err;
  let timestamp = log.timestamp;

  const params = {
    TableName: tableName,
    Item: { deviceID, err, timestamp }
  };

  await docClient.put(params).promise();
  return log;
};

