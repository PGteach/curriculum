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
 *
 * After pasting a new version, run reformatAllTabs() once from the editor to
 * apply the column widths and formatting to tabs that already exist.
 */

var SHEET_ID = "1Y3jeo_5e2Q5r7fYEuTr79Pr8dPEtjmp8pVeqTJabXss";

/**
 * true  -> one tab per lecture ("Lecture 1", "Lecture 2", …), created on demand
 * false -> everything in a single "All results" tab, with a Lecture column
 *
 * USING APPSHEET? Set this to false. AppSheet binds one table to one
 * worksheet and does not discover new tabs by itself, so a tab per lecture
 * means adding a new AppSheet table every single lecture. With one tab you
 * add the table once and filter on the Lecture column. Run mergeTabsIntoOne()
 * after flipping this, to bring the existing per-lecture rows across.
 */
var ONE_TAB_PER_LECTURE = true;

/**
 * The table, in order. Headers, widths, wrapping, alignment and the phone
 * text format are all derived from this, so adding a column is a one-line
 * change and nothing else needs updating.
 *   wrap:  true to wrap long text, false to clip it to the column
 *   align: left | center | right
 *   text:  true to force text format (stops Sheets eating leading zeros)
 */
var COLUMNS = [
  { header: "Submitted at",      width: 150, align: "left"   },
  { header: "Lecture",           width:  95, align: "left"   },
  { header: "Name",              width: 200, align: "left"   },
  { header: "Phone",             width: 130, align: "left",   text: true },
  { header: "Date",              width: 100, align: "center" },
  { header: "Score",             width:  65, align: "center" },
  { header: "Out of",            width:  65, align: "center" },
  { header: "Weak sections",     width: 210, align: "left",   wrap: true },
  { header: "Section breakdown", width: 300, align: "left",   wrap: true },
  { header: "Mistakes",          width: 460, align: "left",   wrap: true },
  { header: "Screenshot",        width: 120, align: "center" }
];

var HEADERS   = COLUMNS.map(function (c) { return c.header; });
var PHONE_COL = HEADERS.indexOf("Phone") + 1;   // 1-based

var INK  = "#16233F";   // header background
var LINE = "#D8DDE4";   // grid lines

/* Drive folder the result cards are filed under. Left private on purpose:
   the cards carry student names and phone numbers, so they stay visible
   only to whoever owns this script. Do not add setSharing here. */
var IMAGE_FOLDER = "PGteach quiz results";

/**
 * Bump this whenever COLUMNS or formatTab_() changes. Every tab records the
 * version it was last formatted at, and the next submission reformats any tab
 * that is behind. That is what keeps the design a rule rather than a chore:
 * nothing in the sheet is ever styled by hand, and existing tabs catch up on
 * their own without anyone running anything.
 */
var DESIGN_VERSION = 3;

/**
 * OPTIONAL, and off unless you create it. If a tab with this name exists, new
 * lecture tabs are copies of it, so anything you set up there by hand carries
 * over. Leave it alone — which is the default — and formatTab_() below is the
 * single source of the design. createTemplateTab() makes one if you ever want
 * to hand-style instead.
 */
var TEMPLATE_TAB = "Template";


function doPost(e) {
  try {
    var d = JSON.parse(e.postData.contents);
    var book = SpreadsheetApp.openById(SHEET_ID);
    var lecture = String(d.lecture || "Unknown lecture").trim();
    var sheet = getSheet_(book, lecture);

    // The row matters more than the picture, so a Drive failure must not
    // cost us the submission.
    var shot = "";
    try {
      shot = saveImage_(d.image, lecture, d.name);
    } catch (imgErr) {
      shot = "(image failed: " + String(imgErr) + ")";
    }

    sheet.appendRow([
      new Date(),
      lecture,
      d.name || "",
      "",                       // phone is written below, as text
      d.date || "",
      d.score,
      d.total,
      d.weak || "",
      d.sections || "",
      formatMistakes_(d.wrongQuestions),
      shot
    ]);

    var row = sheet.getLastRow();

    // Written separately with the cell forced to text first. Through
    // appendRow, Sheets reads "01129907116" as a number and drops the zero.
    sheet.getRange(row, PHONE_COL)
         .setNumberFormat("@")
         .setValue(String(d.phone || ""));

    sheet.getRange(row, 1, 1, COLUMNS.length).setVerticalAlignment("top");

    return json_({ ok: true, tab: sheet.getName(), row: row, image: shot });

  } catch (err) {
    // Note: the quiz sends with mode:"no-cors", so the browser cannot read
    // this. Check the sheet, or Executions in the Apps Script editor.
    return json_({ ok: false, error: String(err) });
  }
}

function doGet() {
  return ContentService.createTextOutput("Quiz results endpoint is running.");
}


/* ------------------------------------------------------------------ */
/* Sheet plumbing                                                      */
/* ------------------------------------------------------------------ */

/** Returns the target tab, creating and formatting it the first time. */
function getSheet_(book, lecture) {
  var name = ONE_TAB_PER_LECTURE ? lecture : "All results";
  var sheet = book.getSheetByName(name);

  if (!sheet) {
    var tpl = book.getSheetByName(TEMPLATE_TAB);
    if (tpl) {
      // Duplicate the hand-styled tab, so its formatting comes along.
      sheet = tpl.copyTo(book).setName(name);
      sheet.showSheet();                       // a copy of a hidden tab is hidden
      if (sheet.getMaxRows() > 1) {            // keep the header, drop any sample rows
        sheet.getRange(2, 1, sheet.getMaxRows() - 1, sheet.getMaxColumns())
             .clearContent();
      }
      if (!isResultsTab_(sheet)) {             // template drifted from COLUMNS
        sheet.getRange(1, 1, 1, HEADERS.length).setValues([HEADERS]);
      }
    } else {
      sheet = book.insertSheet(name);
      sheet.appendRow(HEADERS);
      formatTab_(sheet);
    }
    sortTabs_(book);
  }

  if (sheet.getLastRow() === 0) {
    sheet.appendRow(HEADERS);
    formatTab_(sheet);
    stampDesign_(sheet);
  }

  ensureDesign_(sheet);
  return sheet;
}

/**
 * Reformats a tab if it has not been formatted at the current DESIGN_VERSION.
 * One tiny property read per submission; the reformat itself happens once per
 * tab per version bump. This is what makes the look self-healing.
 */
function ensureDesign_(sheet) {
  try {
    var props = PropertiesService.getScriptProperties();
    var key = "design:" + sheet.getSheetId();
    if (props.getProperty(key) === String(DESIGN_VERSION)) return;
    formatTab_(sheet);
    props.setProperty(key, String(DESIGN_VERSION));
  } catch (e) {
    // Formatting is cosmetic; never let it cost us a submission.
  }
}

function stampDesign_(sheet) {
  try {
    PropertiesService.getScriptProperties()
      .setProperty("design:" + sheet.getSheetId(), String(DESIGN_VERSION));
  } catch (e) {}
}

/**
 * Creates the hand-styled Template tab, formatted from COLUMNS as a starting
 * point. Restyle it however you like afterwards — new lecture tabs copy it.
 */
function createTemplateTab() {
  var book = SpreadsheetApp.openById(SHEET_ID);
  if (book.getSheetByName(TEMPLATE_TAB)) {
    Logger.log("'" + TEMPLATE_TAB + "' already exists. Style it by hand; new " +
               "lecture tabs will copy it as it stands.");
    return;
  }
  var tpl = book.insertSheet(TEMPLATE_TAB);
  tpl.appendRow(HEADERS);
  formatTab_(tpl);
  tpl.hideSheet();
  Logger.log("Created '" + TEMPLATE_TAB + "' (hidden). Unhide it, style it by " +
             "hand, and every new lecture tab will look like it. Run " +
             "reformatAllTabs() to push the same look onto the tabs you " +
             "already have.");
}

/**
 * Copies the Template's look onto an existing tab. Widths, frozen panes, row
 * height and cell formats transfer; banding and conditional-formatting rules
 * do not — those only come across when a tab is created as a copy.
 */
function applyTemplateFormat_(tpl, sheet) {
  var n = HEADERS.length;
  var rows = Math.max(sheet.getMaxRows(), 2);

  for (var c = 1; c <= n; c++) sheet.setColumnWidth(c, tpl.getColumnWidth(c));
  sheet.setFrozenRows(tpl.getFrozenRows());
  sheet.setFrozenColumns(tpl.getFrozenColumns());
  sheet.setRowHeight(1, tpl.getRowHeight(1));

  tpl.getRange(1, 1, 1, n).copyTo(sheet.getRange(1, 1, 1, n), {formatOnly: true});
  // a one-row source tiles down the destination
  tpl.getRange(2, 1, 1, n).copyTo(sheet.getRange(2, 1, rows - 1, n),
                                  {formatOnly: true});
}

/**
 * The whole visual treatment for a results tab. Safe to run repeatedly, and
 * safe on a tab that already holds data — it only touches formatting.
 */
function formatTab_(sheet) {
  var nCols = COLUMNS.length;
  var maxRows = sheet.getMaxRows();

  // Trim stray columns so the table ends where the data ends. AppSheet reads
  // the header row, and trailing blank headers can stop it cold.
  if (sheet.getMaxColumns() > nCols) {
    sheet.deleteColumns(nCols + 1, sheet.getMaxColumns() - nCols);
  }

  // Header
  var head = sheet.getRange(1, 1, 1, nCols);
  head.setValues([HEADERS])
      .setFontWeight("bold")
      .setFontColor("#ffffff")
      .setBackground(INK)
      .setVerticalAlignment("middle")
      .setHorizontalAlignment("left")
      .setWrap(false);
  sheet.setRowHeight(1, 34);
  sheet.setFrozenRows(1);
  sheet.setFrozenColumns(3);        // keep time, lecture and name in view

  // Per-column width, alignment, wrapping, number format
  COLUMNS.forEach(function (c, i) {
    var col = i + 1;
    sheet.setColumnWidth(col, c.width);

    var body = sheet.getRange(2, col, Math.max(maxRows - 1, 1), 1);
    body.setHorizontalAlignment(c.align)
        .setVerticalAlignment("top")
        .setWrap(!!c.wrap);
    if (c.text) body.setNumberFormat("@");
  });

  // Grid + zebra striping over the used range only
  var lastRow = Math.max(sheet.getLastRow(), 1);
  var used = sheet.getRange(1, 1, lastRow, nCols);
  used.setBorder(true, true, true, true, true, true, LINE,
                 SpreadsheetApp.BorderStyle.SOLID);
  used.setFontFamily("Inter").setFontSize(10);

  // applyRowBanding throws if a banding already covers the range
  sheet.getBandings().forEach(function (b) { b.remove(); });
  if (lastRow > 1) {
    used.applyRowBanding(SpreadsheetApp.BandingTheme.LIGHT_GREY, true, false);
    // banding repaints the header, so restore it
    head.setFontWeight("bold").setFontColor("#ffffff").setBackground(INK);
  }
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


/* ------------------------------------------------------------------ */
/* Result screenshots                                                  */
/* ------------------------------------------------------------------ */

/**
 * Decodes the base64 PNG the quiz sends and files it in Drive.
 * Returns the file URL, or a short note when there is no image.
 */
function saveImage_(b64, lecture, name) {
  if (!b64) return "(no image)";

  var bytes = Utilities.base64Decode(b64);
  var safe = String(name || "student").replace(/[\/:*?"<>|\\]/g, " ").trim().slice(0, 60);
  var stamp = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), "yyyy-MM-dd HH-mm-ss");
  var file = folder_(lecture).createFile(
    Utilities.newBlob(bytes, "image/png", lecture + " - " + safe + " - " + stamp + ".png"));

  return file.getUrl();
}

/** The per-lecture subfolder, creating both levels the first time. */
function folder_(lecture) {
  var root = pickOrCreate_(DriveApp.getRootFolder(), IMAGE_FOLDER);
  return pickOrCreate_(root, lecture);
}

function pickOrCreate_(parent, name) {
  var hits = parent.getFoldersByName(name);
  return hits.hasNext() ? hits.next() : parent.createFolder(name);
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

/**
 * True only if row 1 is exactly this table's header row.
 *
 * Checking just A1 is not enough: the legacy "Sheet1" also begins with
 * "Submitted at" but has only the old 8 columns, and formatting it would
 * stamp the 11 new headers over data that does not match them.
 */
function isResultsTab_(sheet) {
  if (sheet.getLastColumn() < HEADERS.length) return false;
  var row = sheet.getRange(1, 1, 1, HEADERS.length).getValues()[0];
  for (var i = 0; i < HEADERS.length; i++) {
    if (String(row[i]).trim() !== HEADERS[i]) return false;
  }
  return true;
}

/** Re-applies widths, wrapping, borders and striping to every results tab. */
function reformatAllTabs() {
  var book = SpreadsheetApp.openById(SHEET_ID);
  var tpl = book.getSheetByName(TEMPLATE_TAB);
  var done = [], skipped = [];
  book.getSheets().forEach(function (sheet) {
    if (sheet.getName() === TEMPLATE_TAB) return;
    if (!isResultsTab_(sheet)) { skipped.push(sheet.getName()); return; }
    if (tpl) applyTemplateFormat_(tpl, sheet);
    else formatTab_(sheet);
    stampDesign_(sheet);
    done.push(sheet.getName());
  });
  if (tpl) Logger.log("Used the '" + TEMPLATE_TAB + "' tab as the source of the look.");
  Logger.log("Reformatted: " + (done.join(", ") || "nothing"));
  if (skipped.length) {
    Logger.log("Left alone (header row does not match this table): " +
               skipped.join(", ") + ". For the old 8-column Sheet1, run " +
               "migrateOldRows() instead.");
  }
}

/**
 * One-off repair: phones that were stored as numbers before the text format
 * was in place lost their leading zero, so "01129907116" reads "1129907116".
 * Only touches cells that are numeric and match an Egyptian mobile with the
 * zero missing (10 digits, starting 10/11/12/15). Everything else is listed
 * and left alone for you to look at. Run it, read the log, check the sheet.
 */
function repairPhones() {
  var book = SpreadsheetApp.openById(SHEET_ID);
  var fixed = [], odd = [];

  book.getSheets().forEach(function (sheet) {
    if (!isResultsTab_(sheet)) return;
    var last = sheet.getLastRow();
    if (last < 2) return;

    var range = sheet.getRange(2, PHONE_COL, last - 1, 1);
    var vals = range.getValues();
    range.setNumberFormat("@");

    for (var i = 0; i < vals.length; i++) {
      var v = vals[i][0];
      if (v === "" || v === null) continue;
      var digits = String(v).replace(/\D/g, "");
      if (typeof v === "number" && /^1[0125]\d{8}$/.test(digits)) {
        vals[i][0] = "0" + digits;
        fixed.push(sheet.getName() + " row " + (i + 2) + ": " + digits +
                   " -> 0" + digits);
      } else {
        vals[i][0] = String(v);
        if (digits.length !== 11 || digits.charAt(0) !== "0") {
          odd.push(sheet.getName() + " row " + (i + 2) + ": " + digits +
                   " (left as is)");
        }
      }
    }
    range.setValues(vals);
  });

  Logger.log("Repaired " + fixed.length + " phone number(s).");
  fixed.forEach(function (l) { Logger.log("  " + l); });
  if (odd.length) {
    Logger.log("Not an Egyptian mobile with a missing zero, so untouched:");
    odd.forEach(function (l) { Logger.log("  " + l); });
  }
}

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
    date: "2026-09-01",
    score: 8,
    total: 10,
    weak: "How computers work",
    sections: "How computers work: 1/2 | Programming & AI terms: 3/3",
    wrongQuestions: [{
      question: "What is the first stage in how a computer handles any task?",
      selected: "Processing",
      correct: "Input",
      why: "Everything starts with input."
    }],
    // a real 2x2 PNG, so the Drive path is exercised too
    image: "iVBORw0KGgoAAAANSUhEUgAAAAIAAAACCAIAAAD91JpzAAAAEElEQVR4nGPgq6kGIgYIBQAa5gQVqws3cwAAAABJRU5ErkJggg=="
  })}});
  Logger.log(out.getContent());
}

/**
 * One-off: copies the old 8-column rows from "Sheet1" into the Lecture 1 tab.
 * Those rows predate the Lecture, Mistakes and Screenshot columns, so those
 * are filled in as "(not recorded)". Phone digits already lost their leading
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
      "(not recorded)",     // Mistakes — column did not exist yet
      "(not recorded)"      // Screenshot — ditto
    ]);
    moved++;
  }
  formatTab_(target);
  Logger.log("Migrated " + moved + " row(s) into " + target.getName());
}

/**
 * One-off, for switching to ONE_TAB_PER_LECTURE = false (the AppSheet-friendly
 * layout): copies every "Lecture N" tab into a single "All results" tab.
 * The originals are left untouched — check the merge, then delete them.
 */
function mergeTabsIntoOne() {
  var book = SpreadsheetApp.openById(SHEET_ID);
  var target = book.getSheetByName("All results");
  if (!target) {
    target = book.insertSheet("All results");
    target.appendRow(HEADERS);
    formatTab_(target);
  }

  var moved = 0;
  book.getSheets().forEach(function (sheet) {
    var name = sheet.getName();
    if (name === "All results") return;
    if (!/^Lecture\s+\d+$/.test(name)) return;
    if (sheet.getRange(1, 1).getValue() !== HEADERS[0]) return;

    var rows = sheet.getDataRange().getValues().slice(1);
    rows.forEach(function (r) {
      if (!r[2] && !r[3]) return;              // no name and no phone: blank
      target.appendRow(r);
      moved++;
    });
  });

  formatTab_(target);
  Logger.log("Merged " + moved + " row(s) into 'All results'. The per-lecture " +
             "tabs were left in place — delete them once you have checked the " +
             "result, and set ONE_TAB_PER_LECTURE = false.");
}
