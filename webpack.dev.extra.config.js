// This webpack config is intended solely for generating the bundle for the extra layouts version of
// dash_cytoscape.dev.js
const config = require('./webpack.config.js');

config.entry = {main: './src/lib/extra_index.js'};
config.output = {filename: 'dash_cytoscape_extra.dev.js'};
config.mode = 'development';

module.exports = config;