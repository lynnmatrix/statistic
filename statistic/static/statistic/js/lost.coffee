React = require 'react'
ReactDOM = require 'react-dom'
FixedDataTable = require 'fixed-data-table'
Loading = require 'react-loading'
Bootstrap = require 'react-bootstrap'

require 'fixed-data-table/dist/fixed-data-table.css'

$ =require 'jquery'

{a, h3, div} = React.DOM

Table = React.createFactory FixedDataTable.Table
Column = React.createFactory FixedDataTable.Column
Cell = React.createFactory FixedDataTable.Cell
_Loading = React.createFactory Loading

LostPageHeader = React.createFactory React.createClass
  displayName: 'LostPageHeader'
  render: ->
    (div {style:{display: 'flex', flexDirection:'row', justifyContent:'space-between'}}, [
      (div {}, "总流失: #{@props.ratio['total']}"),
      (div {}, "全失败: #{@props.ratio["all_fail"]}, #{(@props.ratio['all_fail'] / @props.ratio['total'] * 100).toFixed(2)}%"),
      (div {}, "全成功: #{@props.ratio['all_success']}, #{(@props.ratio['all_success'] / @props.ratio['total'] *100).toFixed(2)}%"),
      (div {}, "全失败中试过QQ/163/126: #{@props.ratio['all_fail_qq_163']}, #{(@props.ratio['all_fail_qq_163'] / @props.ratio['all_fail'] * 100).toFixed(2)}%"),
      (div {}, "全成功且只有一个邮箱: #{@props.ratio['all_success_and_single_mailbox_count']}, #{(@props.ratio['all_success_and_single_mailbox_count'] / @props.ratio['all_success'] * 100 ).toFixed(2)}%")
    ])

_LostTable = React.createFactory React.createClass({
    displayName: 'LostTable'
    render: ->

      data =  []
      for user, all_fail of @props.lost
        data.push {user, 'all_fail': all_fail, 'emails': @props.emails[user]}
      tableHeight = (data.length + 1) * 50
      (div {}, [(Table {rowHeight: 50,headerHeight: 50,rowsCount: data.length, width: @props.tableWidth, height: tableHeight},
        [
          (Column {
            width: 150, header: (Cell {}, "IMEI (共#{@props.ratio['total']}人)"), cell: ((props)->
              (Cell props, (div {href:'#',onClick: ->
                ReactDOM.render (_Loading {type:'bars', color:'#0090e0'}), document.getElementById("config")
                $.getJSON url_config, {imei: data[props.rowIndex]['user']}, (response) ->
                    ReactDOM.render (div {}, [(h3 {}, "配置log"),(ConfigTable {configs: response.configs})]), document.getElementById("config")
              }, data[props.rowIndex]['user']))
            )
          }
          ),
          (Column {
            width: 200, header: (Cell {}, "全失败(#{@props.ratio.all_fail }, #{(@props.ratio.all_fail / @props.ratio.total *100).toFixed(2)}%)"), cell: ((props)->
              (Cell props, if data[props.rowIndex]['all_fail'] then '全失败' else '有成功')
            )
          }
          ),
          (Column {width: 650, flexGrow: 1, header: (Cell {}, 'emails'), cell: ((props)->
              (Cell props, (JSON.stringify data[props.rowIndex]['emails']))
            )}),
        ]
      ), (div {id:'config'})])

  })


_ConfigTable = React.createFactory React.createClass {
  displayName: 'ConfigTable'
  render: ->
    tableHeight = (@props.configs.length + 1) * 50
    configs = @props.configs
    (Table {rowHeight: 50, headerHeight: 50, rowsCount: @props.configs.length, width: @props.tableWidth, height: tableHeight},
      [
        (Column {
          width: 100, header: (Cell {}, "success"), cell: ((props)->
            (Cell props, if configs[props.rowIndex]['issuccess']==0 then 'False'else 'True')
          )
        }
        ),
        (Column {
          width: 100, header: (Cell {}, "autoconfig"), cell: ((props)->
            (Cell props, if configs[props.rowIndex]['isautoconfig']==0 then 'False'else 'True')
          )
        }
        ),
        (Column {
          width: 150, header: (Cell {}, "imei"), cell: ((props)->
            (Cell props, configs[props.rowIndex]['imei'])
          )
        }
        ),
        (Column {
          width: 250, header: (Cell {}, "email"), cell: ((props)->
            (Cell props, configs[props.rowIndex]['email'])
          )
        }
        ),
        (Column {
          width: 100, header: (Cell {}, "protocol"), cell: ((props)->
            (Cell props, if configs[props.rowIndex]['protocol']==1 then 'EAS' else ( if configs[props.rowIndex]['protocol']==2 then "IMAP" else "POP") )
          )
        }
        ),
        (Column {
          width: 250, header: (Cell {}, 'loginname'), cell: ((props)->
            (Cell props, configs[props.rowIndex]['loginname'])
          )
        }),
        (Column {
          width: 400, header: (Cell {}, 'incoming'), cell: ((props)->
            (Cell props, (JSON.stringify configs[props.rowIndex]['incomingconfig']))
          )
        }),
        (Column {
          width: 400, header: (Cell {}, 'outgoing'), cell: ((props)->
            (Cell props, (JSON.stringify configs[props.rowIndex]['outgoingconfig']))
          )
        }),
        (Column {
          width: 200, flexGrow:1, header: (Cell {}, "errormessage"), cell: ((props)->
            (Cell props, configs[props.rowIndex]['errormessage'])
          )
        }
        )
      ]
    )
}

AutoSizableTable = (Component) ->
  React.createFactory React.createClass {
    displayName: 'AutoSizableTable'
    getInitialState: ->
      {tableWidth: 1000}

    componentDidMount: ->
      this._update();
      e = window;
      e.addEventListener("resize", this._onResize, !1)

    _onResize: ->
      clearTimeout(this._updateTimer)
      this._updateTimer = setTimeout(this._update, 16)

    _update: ->
      e = window
      a = if e.innerWidth < 680 then 0 else 240
      this.setState {tableWidth: e.innerWidth - a}

    render: ->
      $ = require 'jquery'
      (Component $.extend({}, @props, @state))
  }

LostTable = AutoSizableTable _LostTable
ConfigTable = AutoSizableTable _ConfigTable

get_next_day_lost = ->

  ReactDOM.render (_Loading {type:'bars', color:'#e3e3e3'}), document.getElementById("content")

  date = $('#date_survival').val()
  interval_unit = $('#interval_unit').val()
  $.getJSON url, {date: date, interval_unit:interval_unit}, (response) ->
    ReactDOM.render (LostPageHeaderF {ratio:response.ratio, date: date}), document.getElementById("header")
    ReactDOM.render (LostTable {lost:response.lost, emails:response.user_emails, ratio:response.ratio}), document.getElementById("content")

window.get_next_day_lost = get_next_day_lost
module.exports.LostPageHeader = LostPageHeader
module.exports.LostTable = LostTable
module.exports.ConfigTable = ConfigTable