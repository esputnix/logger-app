const dynamodb = require('aws-sdk/clients/dynamodb');

const docClient = new dynamodb.DocumentClient();
const tableName = process.env.SAMPLE_TABLE;

exports.putItemHandler = async (event) => {
    const { body, httpMethod, path } = event;
    if (httpMethod !== 'POST') {
        throw new Error(`postMethod only accepts POST method, you tried: ${httpMethod} method.`);
    }
    console.log('received:', JSON.stringify(event));

    const { deviceID, err, timestamp } = JSON.parse(body);

    console.log('received:', JSON.stringify(event));

    console.log('....data:', deviceID, err, timestamp );

    const status = "active";

    const params = {
        TableName: tableName,
        Item: { deviceID, err, timestamp, status },
    };
    await docClient.put(params).promise();

    const response = {
        statusCode: 200,
        body,
    };

    console.log(`response from: ${path} statusCode: ${response.statusCode} body: ${response.body}`);
    return response;
};


[{"error_code": 157, "timestamp": 1577836800}, {"err": 101, "timestamp": 1577836800}]