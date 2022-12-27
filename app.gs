var SS_TITLE = "RoomTempHumidity"
var SHEETNAME = "sheet1"

function doGet(e) {

// Please fill in the link of your Google Sheet here!	
  var ss = SpreadsheetApp.openByUrl("");
  var cell = ss.getRange('A2');
  ss.setCurrentCell(cell);

  sheet = ss.getSheetByName(SHEETNAME);

  var datetime = e.parameter.datetime;
  var humidity = e.parameter.humidity;
  var temperature = e.parameter.temperature;
  
  sheet.appendRow([datetime, humidity,temperature]);
}