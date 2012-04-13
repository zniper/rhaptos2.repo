
// :author: pbrian <paul@mikadosoftware.com>
// :JQuery scripts for ednamode project for CNX.org


// when document is loaded, run this root function, that lisp style will call everything else.... OK.



    function logout(msg){
        // write to a textarea in html
        var txt = $("#logarea").html();
        $("#logarea").html(txt + "<li> " + msg);
    };



    function sendajax(){
	 //constants
         var TGTURL="http://hadrian/e2server/module/";

         var requestmethod = $('input:radio[name=method]:checked').val();
         var payload = {'editortxt':$('#editorarea').val()}; 

	 var menuId = 42;
	 var request = $.ajax({
	     url: TGTURL,
	     type: requestmethod,
             data: payload
	 });

	 request.done(function(data) {
	     $("#responsearea").html(data);      
	     logout('done a success');
	 });

	 request.fail(function(jqXHR, textStatus, err) {
	     logout( "Request failed: " + textStatus + err + jqXHR.status);
	 });

	 request.always(function(jqXHR, textStatus){
	     logout(textStatus);
	 });

    };



$(document).ready(function() {

    var TGTURL="http://hadrian/e2server/module/";
    
    logout('AJAX will fire at ' + TGTURL);    
    $("#click1").click(function(event){
                         sendajax();
                         event.preventDefault();
                       }
                      );

  
});


