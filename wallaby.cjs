// todo: figure out how to run this from the tests/web_ui folder , since it is annoying having to add this to the root of  the repo
//       I was able to make it work ok for KarmaJS but wallabyJS was not working with files outside the tests/web_ui folder folder

module.exports = function (wallaby) {

  return {
    files        : ['./myfeeds_ai/web_ui/js/**/*.*'],
    tests        : ['./tests/web_ui/qunit/**/*.*'             ],
    testFramework: 'qunit',
    env          : { kind: 'chrome'},

    // const path = require('path');
    // middleware: function (app, express) {
    //   console.log(path.resolve(__dirname,'../../myfeeds_ai/web_ui/js/**/*.*'))
    //   app.use(
    //     '/myfeeds_ai',
    //     express.static(path.join(__dirname, '../../myfeeds_ai'))
    //   );
    //},

  };
};