React = require 'react'
FixedDataTable = require 'fixed-data-table'

AutoSizableTable = require './auto-sizable-table.coffee'

{div} = React.DOM

Table = React.createFactory FixedDataTable.Table
Column = React.createFactory FixedDataTable.Column
Cell = React.createFactory FixedDataTable.Cell

SurvivalTable = AutoSizableTable React.createFactory React.createClass {
  displayName: 'SurvivalTable',
  render: ->
    data = @props.survivals

    if data.length > 0
      tableHeight = (data.length + 1) * 50 + 10
      (Table {rowHeight: 50, headerHeight: 50, rowsCount: data.length, width: @props.tableWidth, height: tableHeight}, [
        (Column {
          width: 150, header: (Cell {}, "IMEI (#{@props.survival_count['total'] }, 100%)"), cell: ((props)->
            (Cell props, (div {}, data[props.rowIndex]['imei']))
          )
        }),
        (Column {
          width: 150,
          header: (Cell {}, "1天后 (#{ @props.survival_count['day'] }, #{ (@props.survival_count['day'] / @props.survival_count['total'] * 100).toFixed(2)}%)"),
          cell: ((props)->
            (Cell props, (div {}, if data[props.rowIndex]['survival_day'] then 'True' else 'False'))
          )
        }),
        (Column {
          width: 150,
          header: (Cell {}, "1周后 (#{ @props.survival_count['week'] }, #{ (@props.survival_count['week'] / @props.survival_count['total'] * 100).toFixed(2)}%)"),
          cell: ((props)->
            (Cell props, (div {}, if data[props.rowIndex]['survival_week'] then 'True' else 'False'))
          )
        }),
        (Column {
          width: 150,
          header: (Cell {}, "1月后 (#{ @props.survival_count['month'] }, #{ (@props.survival_count['month'] / @props.survival_count['total'] * 100).toFixed(2)}%)"),
          cell: ((props)->
            (Cell props, (div {}, if data[props.rowIndex]['survival_month'] then 'True' else 'False'))
          )
        }),
        (Column {
          width: 150,
          header: (Cell {}, "1年后 (#{ @props.survival_count['year'] }, #{ (@props.survival_count['year'] / @props.survival_count['total'] * 100).toFixed(2)}%)"),
          cell: ((props)->
            (Cell props, (div {}, if data[props.rowIndex]['survival_year'] then 'True' else 'False'))
          )
        }),
        (Column {
          width: 150,
          header: (Cell {}, "最近一周 (#{ @props.survival_count['last_week'] }, #{ (@props.survival_count['last_week'] / @props.survival_count['total'] * 100).toFixed(2)}%)"),
          cell: ((props)->
            (Cell props, (div {}, if data[props.rowIndex]['survival_last_week'] then 'True' else 'False'))
          )
        }),
      ])
    else
      (div {}, 'No data found')
}

module.exports.SurvivalTable = SurvivalTable