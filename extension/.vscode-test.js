const path = require('path');

module.exports = {
  version: 'stable',
  extensionDevelopmentPath: path.resolve(__dirname),
  extensionTestsPath: path.resolve(__dirname, 'out', 'test', 'suite', 'index'),
  testFiles: [
    path.resolve(__dirname, 'out', 'test', 'suite', 'extension.test.js'),
    path.resolve(__dirname, 'out', 'test', 'suite', 'todo2-watcher.test.js'),
    path.resolve(__dirname, 'out', 'test', 'suite', 'statusbar.test.js')
  ]
};

