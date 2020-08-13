const dynamodb = require('aws-sdk/clients/dynamodb');
const docClient = new dynamodb.DocumentClient();
const tableName = process.env.SAMPLE_TABLE;

exports.getPrevalentHandler = async (event) => {
    const { httpMethod, path } = event;
    if (httpMethod !== 'GET') {
        throw new Error(`getPrevalentHandler only accept GET method, you tried: ${httpMethod}`);
    }
    console.log('received:', JSON.stringify(event));

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
        if (item[1] > 1) {
            result.push(item);
        };
    };

    const response = {statusCode: 200, body: JSON.stringify(result)};

    console.log(`response from: ${path} statusCode: ${response.statusCode} body: ${response.body}`);
    return response;
};
