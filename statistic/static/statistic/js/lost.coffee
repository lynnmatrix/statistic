{a, h3, div} = React.DOM

Table = React.createFactory FixedDataTable.Table
Column = React.createFactory FixedDataTable.Column
Cell = React.createFactory FixedDataTable.Cell

LostPageHeader = React.createFactory React.createClass
  render: ->
    (div {}, [
      (h3 {}, "首次使用时间:#{@props.date}"),
      (div {}, "总流失: #{@props.ratio['total']}"),
      (div {}, "全失败: #{@props.ratio["all_fail"]}, #{(@props.ratio['all_fail'] / @props.ratio['total'] * 100)}%"),
      (div {}, "全成功: #{@props.ratio['all_success']}, #{(@props.ratio['all_success'] / @props.ratio['total'] *100)}%"),
      (div {}, "全失败中试过QQ/163/126: #{@props.ratio['all_fail_qq_163']}, #{(@props.ratio['all_fail_qq_163'] / @props.ratio['all_fail'] * 100)}%"),
      (div {}, "全成功且只有一个邮箱: #{@props.ratio['all_success_and_single_mailbox_count']}, #{(@props.ratio['all_success_and_single_mailbox_count'] / @props.ratio['all_success'] * 100 )}%")
    ])


tableRowClick = (props)->
  s = k for k,v of props


LostTable = React.createFactory React.createClass({
    render: ->
      data =  []
      for user, all_fail of @props.lost
        data.push {user, 'all_fail': all_fail, 'emails': @props.emails[user]}

      (Table {rowHeight: 50,headerHeight: 50,rowsCount: data.length,width: 1000, height: 500},
        [
          (Column {
            width: 150, header: (Cell {}, "IMEI (共#{@props.ratio.total}人)"), cell: ((props)->
              (Cell props, data[props.rowIndex]['user'])
            )
          }
          ),
          (Column {
            width: 100, header: (Cell {}, "成功添加的邮箱(#{@props.ratio.all_fail }, #{@props.ratio.all_fail / @props.ratio.total *100}%"), cell: ((props)->
              (Cell props, if data[props.rowIndex]['all_fail'] then '全失败' else '部分失败')
            )
          }
          ),
          (Column {width: 750, header: (Cell {}, 'emails'), cell: ((props)->
              (Cell props, (JSON.stringify data[props.rowIndex]['emails']))
            )}),
        ]
      )
  })

$ ->
  $.getJSON url, {date: date, interval_unit:interval_unit}, (response) ->
    ReactDOM.render (LostPageHeader {ratio:response.ratio, date: date}), document.getElementById("header")
    ReactDOM.render (LostTable {lost:response.lost, emails:response.user_emails, ratio:response.ratio}), document.getElementById("content")

