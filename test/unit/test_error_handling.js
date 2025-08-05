function getTests() {
  function testTryCatch(result, fail) {
    tryCatch({
      tryFunc: function () {
        result.actual += "try";
        if (fail) fail();
      },
      catchFunc: function (e) {
        result.actual += ",catch";
      },
      finallyFunc: function () {
        result.actual += ",finally";
      },
      okFunc: function () {
        result.actual += ",ok";
      }
    });
  }

  function testTryFinally(result, fail) {
    tryCatch({
      tryFunc: function () {
        result.actual += "outer-try";
        tryFinally({
          tryFunc: function () {
            result.actual += ",try";
            if (fail) fail();
          },
          finallyFunc: function () {
            result.actual += ",finally";
          },
          okFunc: function () {
            result.actual += ",ok";
          }
        });
      },
      catchFunc: function (e) {
        result.actual += ",outer-catch";
      },
      finallyFunc: function () {
        result.actual += ",outer-finally";
      },
      okFunc: function () {
        result.actual += ",outer-ok";
      }
    });
  }

  function testTryRethrow(result) {
    var error;
    tryCatch({
      tryFunc: function () {
        result.actual += "outer-try";
        tryCatch({
          tryFunc: function () {
            result.actual += ",try";
            throwException(error = new Error("test"));
          },
          catchFunc: function (e) {
            result.actual += ",catch";
            result.actual += "(" + (e === error) + ")";
            throwException(e);
          },
          finallyFunc: function () {
            result.actual += ",finally";
          },
          okFunc: function () {
            result.actual += ",ok";
          }
        });
      },
      catchFunc: function (e) {
        result.actual += ",outer-catch";
        result.actual += "(" + (e === error) + ")";
      },
      finallyFunc: function () {
        result.actual += ",outer-finally";
      },
      okFunc: function () {
        result.actual += ",outer-ok";
      }
    });
  }

  return [
    function (result) {
      result.expected = "try,finally,ok";
      testTryCatch(result);
    },
    function (result) {
      result.expected = "try,catch,finally,ok";
      testTryCatch(result,
                   function () { undefined(); });
    },
    function (result) {
      result.expected = "outer-try,try,finally,ok,outer-finally,outer-ok";
      testTryFinally(result);
    },
    function (result) {
      result.expected = "outer-try,try,finally,outer-catch,outer-finally,outer-ok";
      testTryFinally(result,
                     function () { undefined(); });
    },
    function (result) {
      result.expected = "outer-try,try,catch(true),finally,outer-catch(true),outer-finally,outer-ok";
      testTryRethrow(result);
    }
  ];
}

function test() {
  var tests = getTests();
  for (var i = 0; i < tests.length; ++i) {
    var result = {actual: ""};
    tests[i](result);
    assertEqual(result.expected, result.actual);
  }

  tryCatch = tryCatchAsync;
  tryFinally = tryFinallyAsync;
  throwException = throwExceptionAsync;

  var results = new Array(tests.length);
  for (var i = 0; i < tests.length; ++i) {
    (function (i) {
      results[i] = {actual: ""};
      setTimeout(function () {
        log("timeout: " + i);
        tests[i](results[i]);
        log("timeout: " + i);
      }, 100 * i);
    })(i);
  }

  setTimeout(function () {
    var passed = 0;
    for (var i = 0; i < tests.length; ++i) {
      if (results[i].actual == results[i].expected) {
        ++passed;
      } else {
        log("Assertion FAILED:\n" +
            "  expected (" + results[i].expected + ") !== actual (" + results[i].actual + ")",
            "color:orangered;");
      }
    }
    log(passed + " of " + tests.length + " passed");
    assertEqual(null, asyncErrorHandler);
    assertEqual(null, asyncException);
    if (passed == tests.length) {
      log("Test PASSED", "color:green;");
      document.title = "Test PASSED";
    }
  }, 100 * tests.length);

  tryCatch({
    tryFunc: function () { undefined(); },
    catchFunc: function (e) { log("async tests have been initialized"); }
  });
}
