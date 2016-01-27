React = require 'react'
ReactDOM = require 'react-dom'
$ = require 'jquery'
RB = require 'react-bootstrap'
ReactRouter = require 'react-router'

{div, h3, a} = React.DOM

Router = React.createFactory ReactRouter.Router
Link = React.createFactory ReactRouter.Link

Navbar = React.createFactory RB.Navbar
Nav = React.createFactory RB.Nav
NavItem = React.createFactory RB.NavItem

Navbar.Header = React.createFactory RB.Navbar.Header
Navbar.Brand = React.createFactory RB.Navbar.Brand
Navbar.Toggle = React.createFactory RB.Navbar.Toggle
Navbar.Collapse = React.createFactory RB.Navbar.Collapse

App = React.createClass {
  render: ->
    (div {}, [(Navbar {inverse: true}, [
      (Navbar.Header {}, [(Navbar.Brand {}, (Link {to:'#'}, '极邮统计')), (Navbar.Toggle)]),
      (Navbar.Collapse {}, (Nav {}, [
        (NavItem {eventKey:1}, (Link {to:'/lost'}, '流失分析')),
        (NavItem {eventKey:2}, (Link {to:"/usermodel"}, '用户模型')),
        (NavItem {eventKey:3}, (Link {to:"/help"}, '用户求助'))
      ]))
    ]), this.props.children])
}
AppF = React.createFactory App

LostPage = React.createFactory (require './lostpage')

Lost =  React.createClass {
  render: ->
    (LostPage {url_get_lost})
}
LostF = React.createFactory Lost

UserModel =  React.createClass {
  render: ->
    (div {}, 'user model')
}
UserModelF = React.createFactory UserModel

Feedback = React.createClass {
  render: ->
    (div {}, 'feed back')
}
FeedbackF = React.createFactory Feedback


routes = {
  path:'/',
  component: App,
  childRoutes: [
    {path:'lost', component: Lost},
    {path:'usermodel', component: UserModel},
    {path:'help', component: Feedback},
  ]
}
history = ReactRouter.History.createHistory

$(->
  ReactDOM.render (Router {history , routes}), document.getElementById('container')
)
