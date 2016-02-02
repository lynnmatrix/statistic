var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker')

var config = require('./webpack.base.config.js')

// Use webpack dev server
config.entry.app = [
        "webpack-dev-server/client?http://0.0.0.0:8080",
        'webpack/hot/only-dev-server',
        './statistic/static/statistic/js/index.coffee'
    ]

// override django's STATIC_URL for webpack bundles
config.output.publicPath = 'http://0.0.0.0:8080/assets/bundles/'

// Add HotModuleReplacementPlugin and BundleTracker plugins
config.plugins = config.plugins.concat([
  new webpack.HotModuleReplacementPlugin(),
  new webpack.NoErrorsPlugin(),
  new BundleTracker({filename: './webpack-stats.json'}),
])

// Add a loader for JSX files with react-hot enabled
config.module.loaders.push([
        {test: /\.coffee$/, exclude: /node_modules/, loaders: ['react-hot', 'coffee']},
        {test: /\.jsx?$/, exclude: /node_modules/, loaders: ['react-hot', 'babel?presets[]=react']},
        {test: /\.cjsx$/, exclude: /node_modules/, loaders: ['react-hot', 'coffee', 'cjsx']}
    ]
)

module.exports = config
