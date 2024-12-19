module.exports = function (wallaby) {
  return {
    files: [
      './js/**/*.*',

    ],
    tests: [
      './qunit/**/*.*',
    ],
    testFramework: 'qunit',
    env: {
      kind: 'chrome',
    }
  };
};