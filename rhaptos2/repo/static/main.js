// Generated by CoffeeScript 1.3.3
(function() {

  define(['jquery', 'model/tools'], function(jQuery, Tools) {
    var content, loadModel;
    this.jQuery = this.$ = function() {
      console.warn('You should add "jquery" to your dependencies in define() instead of using the global jQuery!');
      return jQuery.apply(this, arguments);
    };
    jQuery.extend(this.jQuery, jQuery);
    content = null;
    loadModel = function() {
      var uuid;
      uuid = jQuery('#uuid').val();
      content = new Tools.Metadata(uuid);
      if (uuid) {
        return content.fetch();
      }
    };
    loadModel();
    jQuery('#uuid').on('change', function() {
      return loadModel();
    });
    jQuery('#metadata-link').on('click', function(evt) {
      var modal;
      evt.preventDefault();
      modal = new Tools.ModalWrapper(new Tools.MetadataEditView({
        model: content
      }), 'Edit Metadata');
      return modal.show();
    });
    return jQuery('#roles-link').on('click', function(evt) {
      var modal;
      evt.preventDefault();
      modal = new Tools.ModalWrapper(new Tools.RolesEditView({
        model: content
      }), 'Edit Roles');
      return modal.show();
    });
  });

}).call(this);
