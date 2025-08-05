function test() {
  var obj = {
    "1": "one",
    "2": "two",
    "3": [1, 2, "three"],
    "four": true,
    "five": false,
    "six": {"null": null, "array": [{}, {}, []]},
    "string_with_special_chars": "t=\t, q=\", a='"
  };
  assertEqual('{' +
              '"1":"one",' +
              '"2":"two",' +
              '"3":[1,2,"three"],' +
              '"four":true,' +
              '"five":false,' +
              '"six":{"null":null,"array":[{},{},[]]},' +
              "\"string_with_special_chars\":\"t=\\t, q=\\\", a='\"" +
              '}',
              JSON2.stringify(obj));
  assertEqual("{\n" +
              " \"1\": \"one\",\n" +
              " \"2\": \"two\",\n" +
              " \"3\": [\n" +
              "  1,\n" +
              "  2,\n" +
              "  \"three\"\n" +
              " ],\n" +
              " \"four\": true,\n" +
              " \"five\": false,\n" +
              " \"six\": {\n" +
              "  \"null\": null,\n" +
              "  \"array\": [\n" +
              "   {},\n" +
              "   {},\n" +
              "   []\n" +
              "  ]\n" +
              " },\n" +
              " \"string_with_special_chars\": \"t=\\t, q=\\\", a='\"\n" +
              "}",
              JSON2.stringify(obj, null, 1));
}
