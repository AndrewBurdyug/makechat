// Load the application once the DOM is ready, using `jQuery.ready`:
$(function(){

    //User Model
    //----------------
    var Login = Backbone.Model.extend({
        idAttribute: '_id',
        url: '/api/login',
        initialize: function() {
            return {
                username: 'test1',
                password: 'test1'
            }
        }

    });

    login = new Login;

    login.on('change:username', function(model, value){
        console.log('new value: %s', value);
    });

    login.set({username: 'test', password: 'test'});

    login.save();
});
