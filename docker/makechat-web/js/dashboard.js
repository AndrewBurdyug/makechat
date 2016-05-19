// Load the application once the DOM is ready, using `jQuery.ready`:
$(function(){

    // Enable Semantic UI tabs
    $('.menu .item').tab();

    // Generic model
    var GenericModel = Backbone.Model.extend({
        idAttribute: '_id'
    });

    // Generic collection of menu items
    var GenericCollection = Backbone.Collection.extend({
        model: function(attrs, options) {
            return new GenericModel(attrs, options);
        },
        url: function() {
            endpoint = $('.active.item').attr('data-tab');
            return endpoint == 'logout' ? '/logout' : '/api/' + endpoint;
        }
    });

    var generic_menu = new GenericCollection;

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
        getDashboardData: function(){
            this.$('#current-page').text('home');
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
        collection: generic_menu
    });
});


