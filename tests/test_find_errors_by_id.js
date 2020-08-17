var AWS = require("aws-sdk");

docClient = new AWS.DynamoDB.DocumentClient({region: 'us-east-1'});
tableName = 'logger-app-SampleTable-I92ZQMWUI63R'

async function find_by_device_id_and_error () {
  let deviceID = "JA3215H14CU015290"
  let error = 56634

  var params = {
    TableName: tableName,
    IndexName: "errIndex",
    KeyConditionExpression:"#deviceID = :deviceIDValue and #err = :errorValue",
    ExpressionAttributeNames: {
      "#deviceID": "deviceID",
      "#err": "err"
    },
    ExpressionAttributeValues: {
      ":deviceIDValue": deviceID,
      ":errorValue": error
    },
    ScanIndexForward: true
  }; 
  let data = await docClient.query(params).promise();
  return data["Items"].sort((a, b) => (a.timestamp > b.timestamp) ? 1 : -1)
}


async function main() {
  // return await lamdaHandler();
  return await find_by_device_id_and_error();
}

main()
.then((result) => {
  console.log("..........main:", result);
});

