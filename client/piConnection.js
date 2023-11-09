const net = require('net');
const express = require('express');
const app = express();
const http = require('http');
var Web3 = require('web3');
const configuration = require('../build/contracts/Sensors.json');
const web3 = new Web3(new Web3.providers.HttpProvider("http://127.0.0.1:7545"));
//const web3 = new Web3(new Web3.providers.HttpProvider("http://block.amaxilatis.com:8545"));
const contract = new web3.eth.Contract(configuration.abi, configuration.networks[5777].address);
const fs = require('fs');
const bodyParser = require('body-parser');
const cors = require('cors');
const { addTemperatureValuePi, addHumidityValuePi, times } = require('../server/app');

app.use(cors());
app.use(express.json());

// const serverIp = 'raspberrypi.local';
const serverIp = '169.254.164.173';
const port = 1050; // port that raspberry pi server runs
const client = new net.Socket();

let cnt = 0;

client.connect(port, serverIp, () => {
    client.write('start'); // Automatically start
});

client.on('data', data => {
    const jsonData = data.toString().trim();
    const parsedData = JSON.parse(jsonData);
    const temperature = parsedData.temperature;
    const humidity = parsedData.humidity;
    if (cnt < 20){
        (async function () {
            let delayT = await addTemperatureValuePi(temperature);
            console.log(delayT);
            let delayH = await addHumidityValuePi(temperature);
            console.log(delayH);
        })();
        cnt += 1;
    } else {
        client.write('stop');
        client.end();
    }
});

// client.on('close', () => {
//     console.log('Connection closed.');
// });
