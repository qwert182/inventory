function assertEqual(expected, actual) {
  if (expected !== actual) {
    var msg = "Assertion FAILED:\n" +
              "  expected (" + expected + ") !== actual (" + actual + ")";
    log(msg, "color:orangered;");
    throwException(new Error(msg));
  }
}
