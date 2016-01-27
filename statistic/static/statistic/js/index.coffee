React = require 'react'
ReactDOM = require 'react-dom'
$ = require 'jquery'
RB = require 'react-bootstrap'
ReactRouter = require 'react-router'

{div} = React.DOM

Router = React.createFactory ReactRouter.Router
Link = React.createFactory ReactRouter.Link

Navbar = React.createFactory RB.Navbar
Nav = React.createFactory RB.Nav
NavItem = React.createFactory RB.NavItem

Navbar.Header = React.createFactory RB.Navbar.Header
Navbar.Brand = React.createFactory RB.Navbar.Brand
Navbar.Toggle = React.createFactory RB.Navbar.Toggle
Navbar.Collapse = React.createFactory RB.Navbar.Collapse

LostPage = React.createFactory (require './lostpage')

App = React.createClass {
  render: ->
    (div {}, [
      (Navbar {inverse: true}, [
        (Navbar.Header {}, [(Navbar.Brand {}, (Link {to: '#'}, '极邮统计')), (Navbar.Toggle {})]),
        (Navbar.Collapse {}, (Nav {}, [
          (NavItem {}, (Link {to: '/lost'}, '流失分析')),
          (NavItem {}, (Link {to: "/usermodel"}, '用户模型')),
          (NavItem {}, (Link {to: "/help"}, '用户求助'))
        ]))
      ]),
      @props.children
    ])
}

Lost =  React.createClass {
  render: ->
    (LostPage {url_get_lost})
}

UserModel =  React.createClass {
  render: ->
    (div {}, 'user model')
}

Feedback = React.createClass {
  render: ->
    (div {}, 'feed back')
}

$(->
  history = ReactRouter.History.createHistory

  routes = {
    path:'/',
    component: App,
    childRoutes: [
      {path:'lost', component: Lost},
      {path:'usermodel', component: UserModel},
      {path:'help', component: Feedback},
    ]
  }
  ReactDOM.render (Router {history , routes}), document.getElementById('container')
)
