var Web3 = require('web3');
const configuration = require('../build/contracts/Sensors.json');
// const web3 = new Web3(new Web3.providers.HttpProvider("http://127.0.0.1:7545"));
const web3 = new Web3(new Web3.providers.HttpProvider("http://block.amaxilatis.com:8545"));
const contract = new web3.eth.Contract(configuration.abi, configuration.networks[5777].address);

function getRandomArbitrary(min, max) {
    let num = Math.random() * (max - min) + min;
    let roundedNum = Math.round(num);
    return roundedNum;
}

async function accounts() {
    try {
        return await web3.eth.getAccounts();
    } catch (err) {
        console.log(err);
    }
}

async function addTemperatureValue(idx, acc) {
    try {
        let startTime = performance.now();
        await contract.methods.addTemperature(getRandomArbitrary(-30, +40)).send({from: acc, gas: 1000000});
        let time = performance.now() - startTime;
        return Math.round(time);
    } catch (err) {
        console.log(err);
    }
}

async function addHumidityValue(idx, acc) {
    try {
        let startTime = performance.now();
        await contract.methods.addHumidity(getRandomArbitrary(0, 100)).send({from: acc, gas: 1000000});
        let time = performance.now() - startTime;
        return Math.round(time);
    } catch (err) {
        console.log(err);
    }
}

module.exports = {
    accounts,
    addTemperatureValue,
    addHumidityValue
};
