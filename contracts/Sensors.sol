// SPDX-License-Identifier: MIT
pragma solidity ^0.8.15;

contract Sensors {
    address public owner = msg.sender;
    
    int256[] public humidity;
    int256[] public temperature;

    //function for add temper value

    function addTemperature(int256 tempVal) public payable {
      int256 val = int256(tempVal);
		  temperature.push(val);
    }

    //function for add humidity value 

    function addHumidity(int256 humVal) public payable {
      int256 val = int256(humVal); 
		  humidity.push(val);
    }

    //latest humidity value

    function humidityLastVal() public view returns(int256 hLast) {
      hLast = humidity[humidity.length -1];
    }

    //if float division can't be done by solidity, two return values
    //function for return average value --public
    
    function temperatureLastVal() public view returns(int256 tLast) { 
		  tLast = temperature[temperature.length -1];
    }
    //return average humidity value
    function humidityAvgVal() public view returns(int256 hAvg, uint256 numOfRecords) { 
      uint i = 0;
      hAvg = 0;
      for(i=0; i<humidity.length; i++){
        hAvg +=humidity[i];
      }
      numOfRecords = humidity.length;
    }

    //return average temperature value
    function temperatureAvgVal() public view returns(int256 tAvg, uint256 numOfRecords) {  
		uint i = 0; 
    tAvg = 0;
    for(i=0; i<temperature.length; i++){
      tAvg +=temperature[i];
    }
      numOfRecords = temperature.length;
}

// function deleteElement(uint index) public {
//     if (index >= temperature.length) return;

//     temperature[index] = temperature[temperature.length - 1];
//     temperature.pop();
// }

}