const path = require('path');
const R = require('ramda');
const WebpackDashDynamicImport = require('@plotly/webpack-dash-dynamic-import');

const packagejson = require('./package.json');

const dashLibraryName = packagejson.name.replace(/-/g, '_');

module.exports = (env, argv) => {
    const asyncChunks = {
        chunks: 'async',
        minSize: 0,
        name(module, chunks, cacheGroupKey) {
            return `${cacheGroupKey}~${chunks[0].name}`;
        }
    };

    const defaults = {
        devtool: 'none',
        externals: {
            react: 'React',
            'react-dom': 'ReactDOM',
            'plotly.js': 'Plotly'
        },
        mode: 'production',
        module: {
            rules: [
                {
                    test: /\.js$/,
                    exclude: /node_modules/,
                    use: {
                        loader: 'babel-loader',
                    },
                },
                {
                    test: /\.css$/,
                    use: [
                        {
                            loader: 'style-loader',
                        },
                        {
                            loader: 'css-loader',
                        },
                    ],
                },
            ],
        },
        output: {
            path: path.resolve(__dirname, dashLibraryName),
            chunkFilename: '[name].js',
            library: dashLibraryName,
            libraryTarget: 'window',
        },
        plugins: [
            new WebpackDashDynamicImport()
        ]
    };

    const base = {
        entry: { main: './src/lib/index.js' },
        output: {
            filename: 'dash_cytoscape.min.js'
        },
        optimization: {
            splitChunks: {
                name: true,
                cacheGroups: {
                    async: asyncChunks
                }
            }
        }
    };

    const extras = {
        entry: { main: './src/lib/extra_index.js' },
        output: {
            filename: 'dash_cytoscape_extra.min.js'
        },
        optimization: {
            splitChunks: {
                name: true,
                cacheGroups: {
                    async_extra: asyncChunks
                }
            }
        }
    };

    return [
        R.mergeDeepRight(defaults, base),
        R.mergeDeepRight(defaults, extras)
    ];
};