var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker')

var config = require('./webpack.base.config.js')

config.output.path = require('path').resolve('./assets/dist/')

config.plugins = config.plugins.concat([
  new BundleTracker({filename: './webpack-stats-prod.json'}),

  // removes a lot of debugging code in React
  new webpack.DefinePlugin({
    'process.env': {
      'NODE_ENV': JSON.stringify('production')
  }}),

  // keeps hashes consistent between compilations
  new webpack.optimize.OccurenceOrderPlugin(),

  // minifies your code
  new webpack.optimize.UglifyJsPlugin({
    compressor: {
      warnings: false
    }
  })
])


// Add a loader for JSX files with react-hot enabled
config.module.loaders.concat([
        {test: /\.coffee$/, exclude: /node_modules/, loaders: ['coffee']},
        {test: /\.jsx?$/, exclude: /node_modules/, loaders: ['babel?presets[]=react']},
        {test: /\.cjsx$/, exclude: /node_modules/, loaders: ['coffee', 'cjsx']}
    ]
)

module.exports = config
