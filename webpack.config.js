var path = require('path');
var webpack = require('webpack');

module.exports = {
    entry: [
        "webpack-dev-server/client?http://0.0.0.0:8080",
        'webpack/hot/only-dev-server',
        './statistic/static/statistic/js/lost.coffee'

    ],
    devtool: "eval",
    debug: true,
    output: {
        path: path.join(__dirname, "statistic/static/statistic/js"),
        filename: 'lost.js'

    },
    resolveLoader: {
        modulesDirectories: ['node_modules']

    },
    plugins: [
        new webpack.HotModuleReplacementPlugin()

    ],
    resolve: {
        extensions: ['', '.js', '.coffee']

    },
    module: {
        loaders: [
            { test: /\.css$/, loaders: ['style', 'css'] },
            { test: /\.coffee$/, loaders: ['react-hot', 'coffee']  }

        ]

    }

};
