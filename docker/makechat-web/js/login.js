// Load the application once the DOM is ready, using `jQuery.ready`:
$(function(){

    //User Model
    //----------------
    var Login = Backbone.Model.extend({
        idAttribute: '_id',
        url: '/api/login'
    });

    login = new Login;

    // Login View
    //----------------
    var LoginView = Backbone.View.extend({
        events: {
            'click button' : 'processForm',
            'focus input': 'resetError',
        },
        serialize: function(){
            return this.$el.serializeObject();
        },
        processForm: function(e) {
            e.preventDefault();
            this.LogIn();
        },
        resetError: function(e){
            if ($(e.target).parent('.field').hasClass('error')) {
                $(e.target).parent('.field').removeClass('error');
                $(e.target).val('');
                if(e.target.id.match(/password/)) {$(e.target).attr('type', 'password')};
            }
        },
        LogIn: function() {
            var data = this.serialize();
            var errors = [];
            _.mapObject(data, function(value, key){
                if (value == '') { errors.push(key) };
            });
            if (errors.length > 0) {
                _.map(errors, function(elem){
                    this.$('#' + elem).addClass('error');
                });
            } else {
                this.model.set(data);
                this.model.save(null, {
                    error: function(model, response, options){
                        desc = response.responseJSON.description;
                        this.$('#username').parent('.field').addClass('error');
                        this.$('#username').val(desc);
                    },
                    success: function(model, response, options) {location.replace('/dashboard');}
                });
            }
        }
    });

    r = new LoginView({
        el: 'form',
        model: login,
    });

});
