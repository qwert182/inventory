function check() {
  if (gh.connected) {
    assertEqual("main", gh.default_branch);
    pass();
    clearInterval(check.interval);
  }
}

function test() {
  modules.dbConnect.urlPattern = "(\\/)(gh)\\/(example)/(repo)";
  var res = gh.init({
    url: "/gh/example/repo",
    token: "test_token_0000"
  });
  assertEqual("undefined", typeof res);
  gh.connect();
  check.interval = setInterval(check, 100);
  return "async_test";
}
