
// <!--
// Copyright (c) Rice University 2012-3
// This software is subject to
// the provisions of the GNU Affero General
// Public License Version 3 (AGPLv3).
// See LICENCE.txt for details.
// -->


(function() {

  define(['underscore', 'backbone', 'app/urls'], function(_, Backbone, URLS) {
    var AuthModel;
    AuthModel = Backbone.Model.extend({
      me: function(usersCollection) {
        var _this = this;
        return _.find(usersCollection, function(user) {
          return _this.isMe;
        });
      },
      isMe: function(user) {
        return userId === user.get('id');
      },
      signOut: function() {
        return this.set('id', null, {
          unset: true
        });
      },
      url: function() {
        return URLS.ME;
      }
    });
    return new AuthModel();
  });

}).call(this);

