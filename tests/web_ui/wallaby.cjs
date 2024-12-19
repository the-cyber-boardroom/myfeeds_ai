module.exports = function (wallaby) {
  const path = require('path');
  return {
    files: [
      'cbr_custom_data_feeds/web_ui/js/**/*.*',

    ],
    tests: [
      './qunit/**/*.*',
    ],
    testFramework: 'qunit',
    env: {
      kind: 'chrome',
    },
    trace: true,
    middleware: function (app, express) {
      // Serve files from the cbr_custom_data_feeds folder
      console.log(__dirname)
      app.use(
        '/cbr_custom_data_feeds',
        express.static(path.join(__dirname, '../../cbr_custom_data_feeds'))
      );
    },

  };
};