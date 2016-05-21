// Load the application once the DOM is ready, using `jQuery.ready`:
$(function(){
    // if user is not superuser, then hide menu for superuser accounts
    if (!user.is_superuser) $('#users-tab').hide();

    // Configuring nunjucks
    var env = nunjucks.configure('templates', { autoescape: true });
    env.addFilter('date', function(obj, fmt) {
        if (obj === undefined) {
            return moment(new Date).format(fmt);
        } else {
            return moment(obj.$date).format(fmt);
        }
    });

    // Enable Semantic UI elements
    $('.menu .item').tab();

    // Room model
    //----------------
    var Room = Backbone.Model.extend({
        idAttribute: '_id',
        defaults: {
            name: user.username + ' room',
            is_visible: true,
            is_open: true
        },
        parse: function(response, options) {
            response._id = response._id.$oid;
            return response;
        }
    });

    // User model
    //----------------
    var User = Backbone.Model.extend({
        idAttribute: '_id',
        defaults: {
            username: 'username',
            is_disabled: false,
            is_superuser: false,
            email: 'username@example.com'
        },
        parse: function(response, options) {
            response._id = response._id.$oid;
            return response;
        }
    });

    // Rooms collection
    //----------------
    var Rooms = Backbone.Collection.extend({
        model: Room,
        url: '/api/rooms',
        parse: function(data) {
            return data.items;
        }
    });

    var rooms = new Rooms;

    // Users collection
    //----------------
    var Users = Backbone.Collection.extend({
        model: User,
        url: '/api/users',
        parse: function(data) {
            return data.items;
        }
    });

    var users = new Users;

    // Rooms view
    //----------------
    var RoomsView = Backbone.View.extend({
        events: {
            'click #rooms-tab': 'render',
            'click #add-room-btn': 'addRoom',
            'click #add-room-save': 'saveRoom',
            'click #add-room-cancel': 'cancelRoom',
        },
        template: env.getTemplate('rooms.html', true),
        initialize: function() {
            this.collection.fetch();
            this.listenTo(this.collection, "add", this.render);
        },
        render: function() {
            this.$('#current-page').text('rooms');
            this.$('#rooms').html(this.template.render(this.collection));
            return this;
        },
        addRoom: function() {
            this.$('#add-room-btn').hide();
            this.$('#add-room-form').show();
            this.$('.ui.checkbox').checkbox();
        },
        cancelRoom: function() {
            this.$('#add-room-form').hide();
            this.$('#add-room-btn').show();
        },
        saveRoom: function() {
            this.collection.create({
                name: this.$('#add-room-form-name').val(),
                is_open: this.$('#add-room-form-open').prop('checked'),
            });
            this.cancelRoom();
        }
    });

    var rooms_view = new RoomsView({
        el: 'body',
        collection: rooms,
    });

    // Users view
    //----------------
    var UsersView = Backbone.View.extend({
        events: {
            'click #users-tab': 'render',
        },
        template: env.getTemplate('users.html', true),
        initialize: function() {
            this.collection.fetch();
        },
        render: function() {
            this.$('#current-page').text('users');
            this.$('#users').html(this.template.render(this.collection));
            return this;
        },
    });

    var users_view = new UsersView({
        el: 'body',
        collection: users
    });

});
