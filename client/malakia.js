

const data = "{\"malakia\": 1, \"vlakeia\": 2} {\"malakia\": 1, \"vlakeia\": 2}" 

const jsonData = data.toString().trim();
console.log(jsonData);

const parsedData = JSON.parse(jsonData);