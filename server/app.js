const express = require('express');
const app = express();
const http = require('http');
const port = 8080;
var Web3 = require('web3');
const configuration = require('../build/contracts/Sensors.json');
const web3 = new Web3(new Web3.providers.HttpProvider("http://127.0.0.1:7545"));
//const web3 = new Web3(new Web3.providers.HttpProvider("http://block.amaxilatis.com:8545"));
const contract = new web3.eth.Contract(configuration.abi, configuration.networks[5777].address);
const fs = require('fs');
const bodyParser = require('body-parser');
const cors = require('cors');
const winston = require('winston');

app.use(cors());
app.use(express.json());


const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: 'logs.log' })
  ]
});

app.use( bodyParser.json() );       // to support JSON-encoded bodies

app.use(bodyParser.urlencoded({     // to support URL-encoded bodies
 extended: true})); 
app.use(cors())

let times = [];
let timeT;
let timeH;


//random number generator
function getRandomArbitrary(min, max) {
  let num = Math.random() * (max - min) + min; 
  let roundedNum = Math.round(num);
  return roundedNum;
}

//get list of Ethereum accounts
var accountList = new Array();

async function accounts() {
  try{
    const accountArray = await web3.eth.getAccounts();
    accountList = accountArray;
    return accountList;
  }catch (err) {
    console.log(err);
  }
}

//ADD VALUES

async function addTemperatureValue(idx) {
  try{
    await accounts();
    let startTime = performance.now();
    await contract.methods.addTemperature(getRandomArbitrary(-30, +40)).send({from: accountList[idx], gas: 1000000});
    let time = performance.now() - startTime;
    timeT = Math.round(time);
    return timeT;
  }catch (err) {
    console.log(err);
  }
}

async function addHumidityValue(idx) {
  try{
    await accounts();
    let startTime = performance.now();
    await contract.methods.addHumidity(getRandomArbitrary(0, 100)).send({from: accountList[1], gas: 1000000});
    let time = performance.now() - startTime;
    timeH = Math.round(time);
    return timeH;
  }catch (err) {
    console.log(err);
  }
}

async function addTemperatureValuePi(val) {
  try{
    await accounts();
    let value = Math.round(val);
    let startTime = performance.now();
    await contract.methods.addTemperature(value).send({from: accountList[9], gas: 1000000});
    let time = performance.now() - startTime;
    timeT = Math.round(time);
    return timeT;
  }catch (err) {
    console.log(err);
  }
}

async function addHumidityValuePi(val) {
  try{
    await accounts();
    let startTime = performance.now();
    await contract.methods.addHumidity(Math.round(val)).send({from: accountList[9], gas: 1000000});
    let time = performance.now() - startTime;
    timeH = Math.round(time);
    return timeH;
  }catch (err) {
    console.log(err);
  }
}

//DELETE VALUES

// async function deleteValues() {
//   try{
//     await contract.methods.deleteElement(5).send({from: '0x0D218582BEabFCA65f892AA3b5Db8F0E84313209', gas: 1000000});
//     console.log("deleted");
//   }catch (err) {
//     console.log(err);
//   }
// }


//READ VALUES

//------------------------------------------------humidity-------------------------------------------------
async function seeLastValueHum (idx) {
    let startTime = performance.now();
    const lastValHum = await contract.methods.humidityLastVal().call({from: accountList[idx]});
    let time = performance.now() - startTime;
    //console.log("Humidity latest value: ", lastValHum);
    return { lastValue: lastValHum };
}

async function seeAvgValueHum (idx) {
    let startTime = performance.now();
    const {hAvg, numOfRecords} = await contract.methods.humidityAvgVal().call({from: accountList[idx]});
    let time = performance.now() - startTime;
    console.log(`time: ${time}ms`);
    const averageH = hAvg / numOfRecords;
    let roundedAverageH = Math.round(averageH * 100) / 100
    console.log("Humidity average value: ", roundedAverageH);
}

//-----------------------------------------temperature----------------------------------------------
async function seeLastValueTemp (idx) {
    let startTime = performance.now();
    const lastValTemp = await contract.methods.temperatureLastVal().call({from: accountList[idx]});
    let time = performance.now() - startTime;
    console.log("Temperature latest value: ", lastValTemp);
}

async function seeAvgValueTemp (idx) {
    let startTime = performance.now();
    const {tAvg, numOfRecords} = await contract.methods.temperatureAvgVal().call({from: accountList[idx]});
    let time = performance.now() - startTime;
    const averageT = tAvg / numOfRecords;
    let roundedAverageT = Math.round(averageT * 100) / 100;
    console.log("Temperature average value: ", roundedAverageT);
}

module.exports = {
  accounts,
  addTemperatureValue,
  addHumidityValue,
  getRandomArbitrary,
  seeLastValueHum,
  seeAvgValueHum,
  seeLastValueTemp,
  seeAvgValueTemp,
  addTemperatureValuePi,
  addHumidityValuePi,
  timeH,
  times,
  timeT
};

if (require.main === module) {
  // Server-related code that should only run when app.js is executed directly
  app.listen(port, ()=>{
    console.log(`Server is runing on port ${port}`)
  });
}