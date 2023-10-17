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

const serverIp = 'raspberrypi.local'; // Replace with the IP address of your Raspberry Pi
const port = 1050; // The same port number you chose on the Raspberry Pi

const client = new net.Socket();

const addPiData = async (piTemp, piHum) => {
    let addTemp = await addTemperatureValuePi(piTemp);
    let addHum = await addHumidityValuePi(piHum);
    console.log("pi added data successfully");
 }

client.connect(port, serverIp, () => {
    console.log('Connected to server.');
    console.log('Type "start" to start receiving data or "stop" to stop.');
});

client.on('data', data => {
    const jsonData = data.toString().trim();
    const parsedData = JSON.parse(jsonData);
    const temperature = parsedData.temperature;
    const humidity = parsedData.humidity;
    
    addPiData(temperature, humidity);
    
    console.log('Received data:');
    console.log(`Temperature: ${temperature}`);
    console.log(`Humidity: ${humidity}`);
});

client.on('close', () => {
    console.log('Connection closed.');
});

process.stdin.on('data', input => {
    const command = input.toString().trim();
    if (command === 'start' || command === 'stop') {
        client.write(command);
    } else {
        console.log('Invalid command. Type "start" to start receiving data or "stop" to stop.');
    }
});