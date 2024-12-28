// todo: figure out how to run this from the tests/web_ui folder , since it is annoying having to add this to the root of  the repo
//       I was able to make it work ok for KarmaJS but wallabyJS was not working with files outside the tests/web_ui folder folder

module.exports = function (wallaby) {

  return {
    files        : [ './myfeeds_ai/web_ui/js/**/*.*',
                     './myfeeds_ai/static/**/*.mjs' ],
    tests        : [ './tests/web_ui/qunit/**/*.*'  ],
    testFramework: 'qunit',
    env          : { kind: 'chrome'},

    // middleware: function (app, express) {
    //   app.use('/static', express.static(require('path').join(__dirname, 'myfeeds_ai/static')));
    // }

  };
};