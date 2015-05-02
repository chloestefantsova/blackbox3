var initBackbone = function () {
  var Router = Backbone.Router.extend({
    routes: {
      'home-ref': 'home',
      'reg-ref': 'reg',
      'teams-ref': 'teams',
      'tasks-ref/:pk': 'tasks',
    },
    
    home: function() {
      $('.menu-button[data-target=#home]').click();
    },
    reg: function() {
      $('.menu-button[data-target=#reg]').click();
    },
    teams: function() {
      $('.menu-button[data-target=#teams]').click();
    },
    tasks: function(pk) {
      $('.menu-button[data-target=#tasks]').click();
      $('a.pk[href="#tasks-ref/'+pk+'"]').click();
    },
  });
  window.router = new Router();
  Backbone.history.start();
};
