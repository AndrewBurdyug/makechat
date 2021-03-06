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
    saved_active_tab = sessionStorage.getItem('dashboard-active-tab');
    if (saved_active_tab) {
        $('#home-tab').tab('change tab', 'home');
        $('#' + saved_active_tab + '-tab').tab('change tab', saved_active_tab);
    }
    $('#current-page').text(saved_active_tab);
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
            'click .delete.room.item': 'deleteRoom',
            'click .make.public': 'unlockRoom',
            'click .make.private': 'lockRoom'
        },
        template: env.getTemplate('rooms.html', true),
        initialize: function() {
            this.collection.fetch();
            this.listenTo(this.collection, "change", this.render);
            this.listenTo(this.collection, "sync", this.render);
            this.listenTo(this.collection, "update", this.render);
        },
        render: function() {
            this.$('#rooms').html(this.template.render(this.collection));
            this.$('.ui .dropdown').dropdown({useLabels: false});
            this.$('.unlock.room, .lock.room, .add-user').popup({inline: true, hoverable: true, position : 'top right'});
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
        },
        deleteRoom: function(e) {
            room_id = e.target.id;
            this.collection.get(room_id).destroy();
        },
        lockRoom: function(e) {
            room_id = e.target.id;
            model = this.collection.get(room_id);
            model.set({is_open: false});
            model.save(model.changed, {patch: true});
        },
        unlockRoom: function(e) {
            room_id = e.target.id;
            model = this.collection.get(room_id);
            model.set({is_open: true});
            model.save(model.changed, {patch: true});
        },
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
            this.$('#users').html(this.template.render(this.collection));
            return this;
        },
    });

    var users_view = new UsersView({
        el: 'body',
        collection: users
    });


    // Logout view
    //---------------
    var LogoutView = Backbone.View.extend({
        events: {
            'click #logout': 'doLogout'
        },
        doLogout: function(){
            var collection = this.collection;
            this.$('.ui.small.modal')
            .modal({
                onApprove: function() {
                    collection.fetch({
                        success: function(collection, response, options) {
                            location.replace('/login');
                        },
                    });
                },
            })
            .modal('show');
        }
    });

    // Dummy logout collection
    //-------------------------
    var Logout = Backbone.Collection.extend({
        url: '/logout',
    });

    var logout = new Logout;

    var logout_view = new LogoutView({
        el: 'body',
        collection: logout
    });

    // Menu tab view, show meta info, e.g. breadcrumbs
    //-------------------------------------------------
    var MenuTabView = Backbone.View.extend({
        events: {
            'click #menu>.item': 'generalTabChanges',
        },
        generalTabChanges: function() {
            active_tab = $('.item.active').attr('data-tab');
            this.$('#current-page').text(active_tab);
            sessionStorage.setItem('dashboard-active-tab', active_tab);
        },
    });

    var menu_tab_view = new MenuTabView({
        el: 'body',
    });
});
