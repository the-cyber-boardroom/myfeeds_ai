let path = require('path');

module.exports = function(config) {
  config.set({
    basePath: '../../',
    frameworks: ['qunit'],
    files: [
        { pattern: 'cbr_custom_data_feeds/web_ui/js/**/*.*'    , type: 'module' },
        { pattern: 'tests/web_ui/qunit/**/*.*' , type: 'module' },
    ],
    exclude: [],
    preprocessors: {
      // You can specify preprocessors here if necessary
    },
    reporters: ['progress'],
    port: 9876,
    colors: true,
    logLevel: config.LOG_INFO,
    //logLevel: config.LOG_DEBUG,
    autoWatch: true,
    browsers: ['ChromeHeadless'],
    singleRun: false,
    concurrency: Infinity,
    proxies: {}
  });
};

