/**
 * Created by linym on 1/29/16.
 */
var path = require("path")
var webpack = require('webpack')


module.exports = {
  context: __dirname,

  entry: {
      app: './statistic/static/statistic/js/index.coffee',
      vendors: ['react', 'react-dom', 'react-bootstrap', 'react-router', 'jquery', 'fixed-data-table/dist/fixed-data-table.css']
  },

  output: {
      path: path.resolve("./assets/bundles/"),
      filename: "[name]-[hash].js"
  },

  plugins: [
      new webpack.optimize.CommonsChunkPlugin('vendors', "[name]-[hash].js")
  ], // add all common plugins here

  module: {
    loaders: [
        { test: /\.css$/, loaders: ['style', 'css'] },
    ] // add all common loaders here
  },

  resolve: {
    modulesDirectories: ['node_modules'],
    extensions: ['', '.js', '.jsx',  '.coffee']
  },
}
