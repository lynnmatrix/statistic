React = require 'react'
ReactDOM = require 'react-dom'
FixedDataTable = require 'fixed-data-table'
Loading = require 'react-loading'

{form, input, div, label, option, button, select} = React.DOM
Table = React.createFactory FixedDataTable.Table
Column = React.createFactory FixedDataTable.Column
Cell = React.createFactory FixedDataTable.Cell
_Loading = React.createFactory Loading

{ButtonGroup, Button} = require 'react-bootstrap'
ButtonGroup = React.createFactory ButtonGroup
Button = React.createFactory Button

{LostPageHeader, LostTable}= require('./lost.coffee')

$ = require 'jquery'
$.ajaxSetup(
    {
        beforeSend: (xhr, settings) ->
            getCookie = (name) ->
                cookieValue = null
                if (document.cookie and document.cookie) isnt ''
                    cookies = document.cookie.split(';')
                    for cookie in cookies
                        if cookie.substring(0, name.length+1) is name+'='
                            cookieValue = decodeURIComponent(
                                cookie.substring(name.length+1)
                            )
                            break
                return cookieValue
            if not (/^http:.*/.test(settings.url) or /^https:.*/.test(settings.url))
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'))
    }
)

LostForm = React.createClass {
  displayName: 'LostForm',
  getInitialState: ->
    {
      date: new Date().toISOString().substring(0, 10)
      interval_unit: '1'
    }

  render: ->
    rowStyle = {display: 'flex', flexDirection:'row', justifyContent: 'space-between'}
    (div {}, [
      (div {style: rowStyle}, [
        (label {}, '时区: Asia/Shanghai'),
        (label {htmlFor: 'date_survival'}, ['首次使用时间: ', (input {
          type: 'date',
          value: @state.date,
          name: 'date',
          id: 'date_survival',
          onChange: @handleDateChange
        })])]),
      (div {style: rowStyle}, [
        (ButtonGroup {bsSize:'small'}, [
          (Button {onClick: @props.onQueryLostRate}, '留存率'),
          (Button {onClick: @props.onQueryLostRate}, '流失用户'),
        ])

        (label {htmlFor: 'interval_unit'}, ['所在的',
          (select {
            name: 'interval_unit',
            id: 'interval_unit',
            value: @state.interval_unit,
            onChange: @handleUnitChange
          }, [
            (option {value: '1'}, '天'),
            (option {value: '2'}, '周'),
            (option {value: '3'}, '月'),
          ])])
      ])
    ])

  handleDateChange: (e)->
    @setState {date: e.target.value}

  handleUnitChange: (e)->
    @setState {interval_unit: e.target.value()}

}
LostFormF = React.createFactory LostForm

LostRateTable = React.createClass {
  displayName: 'LostRateTable',
  render: ->
    data = []
    for imei, user_survival in @props.user_survivals
      data.push user_survival

    if data.length > 0
      tableHeight = (data.length + 1) * 50
      (Table {rowHeight: 50, headerHeight: 50, rowsCount: data.length, width: @props.tableWidth, height: tableHeight}, [
        (Column {
          width: 150, header: (Cell {}, "IMEI (#{@props.survival_count .0 }, 100%)"), cell: ((props)->
            (Cell props, (div {}, data[props.rowIndex]['imei']))
          )
        }),
        (Column {
          width: 150,
          header: (Cell {}, "1天后 (#{ @props.survival_count .1 }, #{ @props.survival_count .1 / @props.survival_count .0 * 100 }%)"),
          cell: ((props)->
            (Cell props, (div {}, data[props.rowIndex]['survival_day']))
          )
        }),
      ])
    else
      (div {}, 'No data found')
}

LostRate = React.createFactory React.createClass {
  displayName: 'LostRate',
  render: ->
    (div {}, [(LostPageHeader {ratio: @props.ratio, date: @props.date}),
      (LostTable {lost: @props.lost, emails: @props.emails, ratio: @props.ratio})
    ])
}

LostPage = React.createClass {
  render: ->
    (div {id:'lost_page', style:{margin:'15px 15px'}}, [
      (LostFormF {onQueryLostRate:@queryLost, user_survivals:{}}),
      (div {id:'lost_rate'})
    ])

  queryLost: ->
    ReactDOM.render (_Loading {type:'bars', color:'#0090e0'}), document.getElementById('lost_rate')

    date = $('#date_survival').val()
    interval_unit = $('#interval_unit').val()
    $.post url_get_lost, {date: date, interval_unit:interval_unit}, (response) ->
      ReactDOM.render (LostRate {date: date, ratio:response.ratio, emails: response.user_emails, lost: response.lost}),
        document.getElementById('lost_rate')
}

module.exports = LostPage;
