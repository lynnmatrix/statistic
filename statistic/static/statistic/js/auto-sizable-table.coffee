React = require 'react'
$ =require 'jquery'

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
      a = if e.innerWidth < 680 then 0 else 40
      this.setState {tableWidth: e.innerWidth - a}

    render: ->
      (Component $.extend({}, @props, @state))
  }

module.exports = AutoSizableTable