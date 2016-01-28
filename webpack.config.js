var path = require('path');
var webpack = require('webpack');

module.exports = {
    entry: [
        "webpack-dev-server/client?http://0.0.0.0:8080",
        'webpack/hot/only-dev-server',
        './statistic/static/statistic/js/user-config.coffee',
        './statistic/static/statistic/js/index.coffee'

    ],
    devtool: "eval",
    debug: true,
    output: {
        path: path.join(__dirname, "statistic/static/statistic/js"),
        filename: 'bundle.js'
    },
    resolveLoader: {
        modulesDirectories: ['node_modules']

    },
    plugins: [
        new webpack.HotModuleReplacementPlugin()

    ],
    resolve: {
        extensions: ['', '.js', '.cjsx', '.coffee']

    },
    module: {
        loaders: [
            { test: /\.css$/, loaders: ['style', 'css'] },
            { test: /\.cjsx$/, loaders: ['react-hot', 'coffee', 'cjsx']},
            { test: /\.coffee$/, loaders: ['react-hot', 'coffee']  }

        ]

    }

};
