// Load the application once the DOM is ready, using `jQuery.ready`:
$(function(){

    // Enable Semantic UI tabs
    $('.menu .item').tab();

    // Room Model
    //-----------
    var Room = Backbone.Model.extend({
        idAttribute: '_id',
    });

    // Rooms Collection
    //-----------------
    var Rooms = Backbone.Collection.extend({
        model: Room,
        url: '/api/rooms'
    });

    var rooms = new Rooms;

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
        collection: rooms
    });
});


