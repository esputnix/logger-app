var AWS = require("aws-sdk");

docClient = new AWS.DynamoDB.DocumentClient({region: 'us-east-1'});
tableName = 'logger-app-SampleTable-I92ZQMWUI63R'


async function getByIdHandler () {
  let deviceID = "JA3215H14CU015290"

  let startDate = '2017-11-05T08:15:30Z'
  let endDate = '2021-11-05T08:15:30Z'
  
  let start_timestamp = new Date(startDate).getTime() / 1000
  let end_timestamp = new Date(endDate).getTime() / 1000
  
  console.log("start_timestamp:", start_timestamp)
  console.log("end_timestamp:", end_timestamp)

  var params = {
    ExpressionAttributeValues: {
      ':s': deviceID,
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
  console.log("...end items ..", data.Items.length);

  let result = [];
  for (let i = 0; i < data.Items.length; i++) {
      let item = data.Items[i];
      console.log(".....", item);
      result.push({"error_code": item.err, "timestamp": item.timestamp });
  }

  console.log("...end result ..", result.length);

  const response = {
    statusCode: 200,
    body: JSON.stringify(result),
  };
  return response;

};

async function main() {
  let result = await getByIdHandler();
  return result;
}

main()
.then((result) => {
  console.log("..........main:", result);
});

