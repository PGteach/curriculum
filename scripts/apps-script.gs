/**
 * PGteach — quiz results collector.
 *
 * Deploy: Extensions > Apps Script, paste this in, Deploy > New deployment >
 * Web app, "Execute as: Me", "Who has access: Anyone", then copy the /exec URL
 * into RESULTS_URL in each lectureN/quiz/index.html.
 *
 * IMPORTANT: after editing this file you must create a NEW deployment (or
 * "Manage deployments" > edit > Version: New version). Saving alone does not
 * update the live /exec URL.
 */

var SHEET_ID = "1Y3jeo_5e2Q5r7fYEuTr79Pr8dPEtjmp8pVeqTJabXss";

/**
 * true  -> one tab per lecture ("Lecture 1", "Lecture 2", …), created on demand
 * false -> everything in a single "All results" tab, with a Lecture column
 * Either way a Lecture column is written, so nothing is lost if you switch.
 */
var ONE_TAB_PER_LECTURE = true;

var HEADERS = [
  "Submitted at",
  "Lecture",
  "Name",
  "Phone",
  "Date",
  "Score",
  "Out of",
  "Weak sections",
  "Section breakdown",
  "Mistakes"
];

var PHONE_COL = 4;   // 1-based index of "Phone" in HEADERS

function doPost(e) {
  try {
    var d = JSON.parse(e.postData.contents);
    var book = SpreadsheetApp.openById(SHEET_ID);
    var lecture = String(d.lecture || "Unknown lecture").trim();
    var sheet = getSheet_(book, lecture);

    sheet.appendRow([
      new Date(),
      lecture,
      d.name || "",
      String(d.phone || ""),
      d.date || "",
      d.score,
      d.total,
      d.weak || "",
      d.sections || "",
      formatMistakes_(d.wrongQuestions)
    ]);

    return json_({ ok: true, tab: sheet.getName() });

  } catch (err) {
    // Note: the quiz sends with mode:"no-cors", so the browser cannot read
    // this. Check the sheet, or Executions in the Apps Script editor.
    return json_({ ok: false, error: String(err) });
  }
}

function doGet() {
  return ContentService.createTextOutput("Quiz results endpoint is running.");
}

/** Returns the target tab, creating and formatting it the first time. */
function getSheet_(book, lecture) {
  var name = ONE_TAB_PER_LECTURE ? lecture : "All results";
  var sheet = book.getSheetByName(name);

  if (!sheet) {
    sheet = book.insertSheet(name);
    sortTabs_(book);
  }

  if (sheet.getLastRow() === 0) {
    sheet.appendRow(HEADERS);
    sheet.getRange(1, 1, 1, HEADERS.length).setFontWeight("bold");
    sheet.setFrozenRows(1);
    // Phone must be text, or Sheets reads "01129907116" as a number and
    // silently drops the leading zero.
    sheet.getRange(1, PHONE_COL, sheet.getMaxRows(), 1).setNumberFormat("@");
    sheet.setColumnWidth(1, 130);   // Submitted at
    sheet.setColumnWidth(3, 170);   // Name
    sheet.setColumnWidth(10, 420);  // Mistakes
  }

  return sheet;
}

/** Keeps lecture tabs in numeric order: Lecture 1, Lecture 2, Lecture 10. */
function sortTabs_(book) {
  var tabs = book.getSheets().slice().sort(function (a, b) {
    return lectureNum_(a.getName()) - lectureNum_(b.getName());
  });
  for (var i = 0; i < tabs.length; i++) {
    book.setActiveSheet(tabs[i]);
    book.moveActiveSheet(i + 1);
  }
}

function lectureNum_(name) {
  var m = String(name).match(/(\d+)/);
  return m ? parseInt(m[1], 10) : 9999;   // non-lecture tabs sink to the end
}

/** wrongQuestions is an array of objects; flatten it into one readable cell. */
function formatMistakes_(list) {
  if (!list || !list.length) return "none";
  return list.map(function (w, i) {
    return (i + 1) + ". " + w.question +
           "\n   chose: " + w.selected +
           "\n   correct: " + w.correct;
  }).join("\n\n");
}

function json_(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

/* ------------------------------------------------------------------ */
/* Run these by hand from the editor, not from the web app.           */
/* ------------------------------------------------------------------ */

/** Check the script can reach the spreadsheet. */
function testSheetAccess() {
  var book = SpreadsheetApp.openById(SHEET_ID);
  Logger.log("Spreadsheet: " + book.getName());
  Logger.log("Tabs: " + book.getSheets().map(function (s) { return s.getName(); }).join(", "));
}

/** Write one fake submission, so you can see the columns fill up. */
function testSubmission() {
  var out = doPost({ postData: { contents: JSON.stringify({
    lecture: "Lecture 1",
    name: "TEST ROW — delete me",
    phone: "01129907116",
    date: "2026-08-31",
    score: 8,
    total: 10,
    weak: "How computers work",
    sections: "How computers work: 1/2 | Programming & AI terms: 3/3",
    wrongQuestions: [{
      question: "What is the first stage in how a computer handles any task?",
      selected: "Processing",
      correct: "Input",
      why: "Everything starts with input."
    }]
  })}});
  Logger.log(out.getContent());
}

/**
 * One-off: copies the old 8-column rows from "Sheet1" into the Lecture 1 tab.
 * Those rows predate the Lecture and Mistakes columns, so both are filled in
 * as "Lecture 1" and "(not recorded)". Phone digits already lost their leading
 * zero when Sheets stored them as numbers and cannot be recovered.
 * Run once, check the result, then delete Sheet1 yourself.
 */
function migrateOldRows() {
  var book = SpreadsheetApp.openById(SHEET_ID);
  var old = book.getSheetByName("Sheet1");
  if (!old) { Logger.log("No Sheet1 to migrate."); return; }

  var rows = old.getDataRange().getValues();
  if (rows.length < 2) { Logger.log("Sheet1 has no data rows."); return; }

  var target = getSheet_(book, "Lecture 1");
  var moved = 0;

  for (var i = 1; i < rows.length; i++) {
    var r = rows[i];
    if (!r[1] && !r[2]) continue;              // skip blank rows
    target.appendRow([
      r[0],                 // Submitted at
      "Lecture 1",
      r[1],                 // Name
      String(r[2] || ""),   // Phone
      r[3],                 // Date
      r[4],                 // Score
      r[5],                 // Out of
      r[6],                 // Weak sections
      r[7],                 // Section breakdown
      "(not recorded)"      // Mistakes — column did not exist yet
    ]);
    moved++;
  }
  Logger.log("Migrated " + moved + " row(s) into " + target.getName());
}
