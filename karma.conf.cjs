

module.exports = function(config) {
  config.set({

    frameworks: ['qunit'],
    files: [
        { pattern: 'myfeeds_ai/static/**/*.mjs'       , type: 'module' },
        { pattern: 'myfeeds_ai/web_ui/js/**/*.*'    , type: 'module' },
        { pattern: 'tests/web_ui/qunit/**/*.*'      , type: 'module' },
    ],
    exclude: [],
    preprocessors: { },
    reporters: ['progress'],
    port: 9876,
    colors: true,
    logLevel: config.LOG_INFO,
    //logLevel: config.LOG_DEBUG,
    autoWatch: true,
    browsers: ['ChromeHeadless'],
    singleRun: false,
    concurrency: Infinity,
    // proxies: { '/myfeeds_ai/': '/base/myfeeds_ai/web_ui' }
  });
};

// todo: figure out how to run this from the tests/web_ui folder , since it is annoying having to add this to the root of  the repo
//       I was able to make it work ok for KarmaJS (using basePath) but wallabyJS was not working with files outside the tests/web_ui folder folder

//let path = require('path');
//    basePath: '../../',