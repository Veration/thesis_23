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
const { seeLastValueHum } = require('../server/app');

app.use(cors());
app.use(express.json());
let attack_iter = 0;

const theInterval = setInterval(async () => {
    if (attack_iter > 50){
        clearInterval(theInterval);
        return;
      }
    let tempLastValue = await seeLastValueHum(process.argv[2]);
    attack_iter++;
}, 3000);
