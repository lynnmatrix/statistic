React = require 'react'
ReactDOM = require 'react-dom'
Loading = require 'react-loading'

{input, div, label, option, select} = React.DOM
_Loading = React.createFactory Loading

{ButtonGroup, Button} = require 'react-bootstrap'
ButtonGroup = React.createFactory ButtonGroup
Button = React.createFactory Button

{LostUserConfigs}= require('./user-config.coffee')
{SurvivalTable} = require './survival-rate.coffee'

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

LostPage = React.createClass {
  render: ->
    (div {id:'lost_page', style:{margin:'15px 15px'}}, [
      (LostForm {onQuerySurvivalRate:@queryLost, onQueryLostUsers:@queryLostUsers}),
      (div {id:'lost_content', style:{
        marginTop:'20px'
      }})
    ])

  queryLost: ->
    @showLoading()

    $.post url_get_survivals, @getQueryParams(), (response) ->
      ReactDOM.render (SurvivalTable {survivals: response.survivals, survival_count: response.survival_count}),
        document.getElementById('lost_content')

  queryLostUsers: ->
    @showLoading()

    $.post url_get_lost, @getQueryParams(), (response) ->
      ReactDOM.render (LostUserConfigs {ratio: response.ratio, lost: response.lost, emails:response.user_config_logs}),
        document.getElementById('lost_content')

  getQueryParams: ->
    date = $('#date_survival').val()
    interval_unit = $('#interval_unit').val()
    {date: date, interval_unit:interval_unit}

  showLoading: ->
    ReactDOM.render (_Loading {type:'bars', color:'#0090e0'}), document.getElementById('lost_content')
}

LostForm = React.createFactory React.createClass {
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
          (Button {onClick: @props.onQuerySurvivalRate}, '留存率'),
          (Button {onClick: @props.onQueryLostUsers}, '流失用户'),
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


module.exports = LostPage;
