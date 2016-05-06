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

    // Room View
    //----------------
    var RoomView = Backbone.View.extend({
        className: 'sidebar',
        events: {
            'click #rooms-tab' : 'getRooms',
        },
        getRooms: function(){
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

    var r = new RoomView({
        el: 'body',
        collection: rooms
    });
});


