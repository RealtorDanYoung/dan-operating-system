/**
 * Writes a lead row into a Google Sheet.
 * Update SHEET_NAME as needed.
 */
function appendLeadRow(name, phone, email, interestType, notes) {
  var SHEET_NAME = 'Leads';
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME);

  if (!sheet) {
    throw new Error('Sheet not found: ' + SHEET_NAME);
  }

  var timestamp = new Date();
  sheet.appendRow([timestamp, name, phone, email, interestType, notes]);
  Logger.log('Lead row added for %s (%s)', name, email);
}

/**
 * Example installable trigger setup:
 * 1) Open Apps Script editor linked to your Google Sheet.
 * 2) Run createDailySummaryTrigger() once and approve permissions.
 */
function createDailySummaryTrigger() {
  ScriptApp.newTrigger('dailySummaryStub')
    .timeBased()
    .everyDays(1)
    .atHour(18)
    .create();
}

/**
 * Trigger target stub for future daily automation tasks.
 */
function dailySummaryStub() {
  Logger.log('Daily summary trigger fired at %s', new Date());
}
