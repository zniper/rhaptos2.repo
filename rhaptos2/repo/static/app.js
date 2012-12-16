// Generated by CoffeeScript 1.3.3
(function() {

  define(['jquery', 'aloha', 'app/views'], function(jQuery, Aloha, Views) {
    var content, loadModel;
    this.jQuery = this.$ = function() {
      console.warn('You should add "jquery" to your dependencies in define() instead of using the global jQuery!');
      return jQuery.apply(this, arguments);
    };
    jQuery.extend(this.jQuery, jQuery);
    Aloha.ready(function() {
      Aloha.jQuery('.document').aloha().focus();
      jQuery('math').wrap('<span class="math-element aloha-cleanme"></span>');
      return MathJax.Hub.Configured();
    });
    content = null;
    loadModel = function() {
      var uuid;
      uuid = jQuery('#uuid').val();
      if (uuid) {
        content = new Views.Module({
          id: uuid,
          url: "/module/" + uuid + "/metadata/"
        });
        return content.fetch();
      } else {
        return content = new Views.Module();
      }
    };
    loadModel();
    jQuery('#uuid').on('change', function() {
      return loadModel();
    });
    jQuery('#metadata-link').on('click', function(evt) {
      var modal;
      evt.preventDefault();
      modal = new Views.ModalWrapper(new Views.MetadataEditView({
        model: content
      }), 'Edit Metadata');
      return modal.show();
    });
    return jQuery('#roles-link').on('click', function(evt) {
      var modal;
      evt.preventDefault();
      modal = new Views.ModalWrapper(new Views.RolesEditView({
        model: content
      }), 'Edit Roles');
      return modal.show();
    });
  });

}).call(this);
