// Load the application once the DOM is ready, using `jQuery.ready`:
$(function(){

    // Configuring nunjucks
    var env = nunjucks.configure('templates', { autoescape: true });
    env.addFilter('date', function(obj, fmt) {
        return moment(obj.$date).format(fmt);
    });

    // Enable Semantic UI tabs
    $('.menu .item').tab();

    // Generic model
    var GenericItem = Backbone.Model.extend({
        idAttribute: '_id',
        defaults: function() {
            endpoint = $('.active.item').attr('data-tab');
            if (endpoint == 'home') {
                return {
                    name: 'tab name',
                    icon: 'star',
                    title: 'Tab'
                };
            };
            if (endpoint == 'rooms') {
                return {
                    name: user.username + ' room',
                    is_visible: true,
                    is_open: true
                };
            };
        }
    });

    var generic_item = new GenericItem;

    // Generic collection of menu items
    var GenericCollection = Backbone.Collection.extend({
        model: function(attrs, options){
            return new GenericItem(attrs, options);
        },
        url: function() {
            endpoint = $('.active.item').attr('data-tab');
            return endpoint == 'logout' ? '/logout' : '/api/' + endpoint;
        },
        parse: function(data) {
            return data.items;
        }
    });

    var generic_collection = new GenericCollection;

    // fetch menu tab items, because the home tab is active by default
    generic_collection.fetch();

    // Menu View
    //----------------
    var GenericView = Backbone.View.extend({
        events: {
            'click #messages-tab, #rooms-tab, #users-tab, #settings-tab': 'showItems',
            'click #home-tab': 'resetChanges',
            'click #logout-tab': 'doLogout'
        },
        template: function() {
            active_tab = this.$('.active.item').attr('data-tab');
            if (active_tab == 'home') return env.getTemplate('menu.html', true);
            if (active_tab == 'rooms') return env.getTemplate('rooms.html', true);
            if (active_tab == 'users') return env.getTemplate('users.html', true);
        },
        showItems: function() {
            this.getItems();
            this.render();
        },
        getItems: function(){
            active_tab = this.$('.active.item').attr('data-tab');
            if (active_tab == 'rooms' && !user.have_rooms) this.collection.reset();
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
            if (this.collection.length == 0) {
                this.collection.create();
                user.have_rooms = true;
            };
            console.log(this.collection);
        },
        render: function() {
            active_tab = this.$('.active.item').attr('data-tab');
            this.$('#current-page').text(active_tab);
            if (active_tab == 'home') this.renderMenu();
            if (active_tab == 'messages') this.renderMessages();
            if (active_tab == 'rooms') this.renderRooms();
            if (active_tab == 'users') this.renderUsers();
            if (active_tab == 'settings') this.renderSettings();
            return this;
        },
        renderMenu: function() {
            this.$('#menu').html(this.template().render(this.collection));
            this.$('.menu .item').tab();
            this.$('#home-tab').toggleClass('active');
        },
        renderMessages: function(){

        },
        renderRooms: function(){
            this.$('#rooms').html(this.template().render(this.collection));
        },
        renderUsers: function(){
            this.$('#users').html(this.template().render(this.collection));
        },
        renderSettings: function(){

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
        resetChanges: function() {
            this.$('#current-page').text('home');
        }
    });

    var r = new GenericView({
        el: 'body',
        collection: generic_collection
    });

    r.render();
    generic_collection.reset();
});
