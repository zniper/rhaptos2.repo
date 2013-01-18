define ['underscore', 'backbone', 'app/urls'], (_, Backbone, URLS) ->
  # Create a singleton model that represents the authenticated user.

  # For the UI, provide a backbone "interface" to the auth piece
  AuthModel = Backbone.Model.extend

    # Returns the `User` model corresponding to the currently logged-in user
    me: (usersCollection) ->
      _.find usersCollection, (user) => @isMe

    isMe: (user) ->
      userId == user.get 'id'

    signOut: ->
      @set 'id', null, {unset: true}

    # To see who the current user is, make an AJAX call to `/me`
    url: -> URLS.ME

  return new AuthModel()
