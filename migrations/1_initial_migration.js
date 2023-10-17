const Sensors = artifacts.require("Sensors");

module.exports = function(_deployer) {
  _deployer.deploy(Sensors);
};