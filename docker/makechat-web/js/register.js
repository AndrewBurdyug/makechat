// Load the application once the DOM is ready, using `jQuery.ready`:
$(function(){

    // User Model
    //----------------
    var User = Backbone.Model.extend({
        idAttribute: '_id',
        url: '/api/register',
    });

    user = new User;

    // SignUp View
    //----------------
    var SignUpView = Backbone.View.extend({
        events: {
            'click button' : 'processForm',
            'focus input': 'resetError',
        },
        serialize: function(){
            return this.$el.serializeObject();
        },
        processForm: function(e) {
            e.preventDefault();
            this.signUp();
        },
        resetError: function(e){
            if ($(e.target).hasClass('error')) {
                $(e.target).removeClass('error');
                $(e.target).val('');
                if(e.target.id.match(/password/)) {$(e.target).attr('type', 'password')};
            }
        },
        signUp: function() {
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
                        elem = desc.match(/password|email|username/i)[0].toLowerCase();
                        if (elem == 'password') {
                            this.$('#password1, #password2').attr('type', 'text').addClass('error').val(desc);
                        } else {
                            this.$('#' + elem).addClass('error').val(desc);
                        }
                    }
                });
            }
        }
    });

    r = new SignUpView({
        el: 'form',
        model: user,
    });

});
