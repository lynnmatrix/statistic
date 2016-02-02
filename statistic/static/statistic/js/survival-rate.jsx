'use strict';

var React = require('react');
var rd3 = require('react-d3');
var LineChart = rd3.LineChart;

var SurvivalRateChart = React.createClass({
    render: function () {

        return (
            <div>
                <LineChart
                    legend={true}
                    data={this.props.rateData}
                    width={600}
                    height={400}
                    viewBoxObject={{x: 0, width: 500, height: 400 }}
                    title="Survival Rate Chart"
                    yAxisLabel="Survival Rate"
                    xAxisLabel="Time"
                    gridHorizontal={true}
                />

                <LineChart
                    legend={true}
                    data={this.props.lineData}
                    width={600}
                    height={400}
                    viewBoxObject={{x: 0, width: 500, height: 400 }}
                    title="Survival Chart"
                    yAxisLabel="Survival Users"
                    xAxisLabel="Time"
                    gridHorizontal={true}
                />


            </div>)
    }
});

module.exports = SurvivalRateChart;

