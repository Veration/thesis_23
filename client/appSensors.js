const express = require('express');
const app = express();
const http = require('http');
var Web3 = require('web3');
const configuration = require('../build/contracts/Sensors.json');
// const web3 = new Web3(new Web3.providers.HttpProvider("http://127.0.0.1:7545"));
const OPTIONS = {
  defaultBlock: "latest",
  transactionBlockTimeout: 150
};
const web3 = new Web3(new Web3.providers.HttpProvider("http://block.amaxilatis.com:8545"), null, OPTIONS);
const contract = new web3.eth.Contract(configuration.abi, configuration.networks[5777].address);
const fs = require('fs');
const bodyParser = require('body-parser');
const cors = require('cors');
const {accounts, addTemperatureValue, addHumidityValue} = require('../server/utils');

app.use(cors());
app.use(express.json());

let cnt1 = 0;
let cnt2 = 0;

const myIndex = process.argv[2];
console.log('MyIndex: ' + myIndex);

let times = [];

const timeout = 1000;

(async function () {
  accountsList = await accounts();
  const myAccount = accountsList[myIndex];
  console.log(myAccount);

  async function addTemperature(){
    let theTimeT = await addTemperatureValue(myIndex, myAccount);
    // times.push(theTimeT);
    console.log(theTimeT + " " + cnt1);
    cnt1 += 1;
    if (cnt1 < 100) {
      setTimeout(addTemperature, theTimeT)
    }
  }

  async function addHumidity(){
    let theTimeH = await addHumidityValue(myIndex, myAccount);
    // times.push(theTimeH);
    console.log(theTimeH + " " + cnt2);
    cnt2 += 1;
    if (cnt2 < 100) {
      setTimeout(addHumidity, theTimeH)
    }
  }

  addTemperature();
  addHumidity();

})();
