// Load the application once the DOM is ready, using `jQuery.ready`:
$(function(){

    // Configuring nunjucks
    var env = nunjucks.configure('templates', { autoescape: true });

    // Enable Semantic UI tabs
    $('.menu .item').tab();

    // Generic model
    var MenuItem = Backbone.Model.extend({
        idAttribute: '_id',
        defaults: {
            name: 'tab name',
            icon: 'star',
            title: 'Tab'
        }
    });

    var menu_item = new MenuItem;

    // Generic collection of menu items
    var Menu = Backbone.Collection.extend({
        model: MenuItem,
        url: function() {
            endpoint = $('.active.item').attr('data-tab');
            return endpoint == 'logout' ? '/logout' : '/api/' + endpoint;
        },
        parse: function(data) {
            return data.items;
        }
    });

    var menu = new Menu;

    menu.fetch();

    // Menu View
    //----------------
    var MenuView = Backbone.View.extend({
        className: 'menu',
        events: {
            'click #home-tab': 'getDashboardData',
            'click #messages-tab': 'getMessages',
            'click #rooms-tab' : 'getRooms',
            'click #users-tab': 'getUsers',
            'click #settings-tab': 'getSettings',
            'click #logout-tab': 'doLogout'
        },
        template: env.getTemplate('menu.html', true),
        render: function() {
            this.$('#menu').html(this.template.render(this.collection));
            this.$('.menu .item').tab();
            this.$('#home-tab').toggleClass('active');
            return this;
        },
        getDashboardData: function(){
            this.$('#current-page').text('home');
            this.collection.fetch(
                {
                    error: function(collection, response, options){
                        if (response.status == 401){
                            location.replace('/login');
                        }
                    },
                    success: function(collection, response, options) {

                    }
                }
            );
        },
        getMessages: function(){
            this.$('#current-page').text('messages');
        },
        getUsers: function(){
            this.$('#current-page').text('users');
        },
        getSettings: function(){
            this.$('#current-page').text('settings');
        },
        doLogout: function(){
            var collection = this.collection;
            this.$('.ui.small.modal')
            .modal({
                onApprove: function() {
                    console.log('logout');
                    collection.fetch({
                        success: function(collection, response, options) {
                            location.replace('/login');
                        }
                    });
                }
            })
            .modal('show');
        },
        getRooms: function(){
            this.$('#current-page').text('rooms');
            this.collection.fetch(
                {
                    error: function(collection, response, options){
                        if (response.status == 401){
                            location.replace('/login');
                        }
                    },
                    success: function(collection, response, options) {

                    }
                }
            );
        }
    });

    var r = new MenuView({
        el: 'body',
        collection: menu
    });

    r.render();
});
