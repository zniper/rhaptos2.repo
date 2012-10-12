// Copyright (c) Rice University 2012
// This software is subject to
// the provisions of the GNU Lesser General
// Public License Version 2.1 (LGPL).
// See LICENCE.txt for details.
//


    var REPOBASEURL = 'http://' + FROZONE.e2repoFQDN;
    var MODULEURL = 'http://' + FROZONE.e2repoFQDN + '/module/';
    var WORKSPACEURL = 'http://' + FROZONE.e2repoFQDN + '/workspace/';

    var PERSONAURL = 'http://' + FROZONE.e2repoFQDN + '/persona/login/';
    var PERSONALOGOUT = 'http://' + FROZONE.e2repoFQDN + '/persona/logout/';


    function logout(msg) {
        //log to a HTML area all messages
        var smsg = '';

        if (typeof(msg) == 'object') {
            for (var item in msg){
                smsg += item + "-" + msg[item];
                                 }
                                     }
        else                         {
            smsg = msg;
                                     }
        var txt = $('#logarea').html();
        $('#logarea').html(txt + '<li> ' + smsg);
        console.log(smsg);
    }

    function get_username() {
        return $('#username').val();
    }

    function get_title() {
        var mname = $('#title').val();
        return mname;
    }

function save_validate() {
    var t = get_title();
    if (t === '') {
        alert('Must have a title');
    }
    return;
}

function get_textarea_html5() {
        //retrieve, as JSON, the contents of the edit-area
        var txtarea = $('#editarea-aloha').html();
        return txtarea;
    }


function load_textarea(mhashid) {
        //

        var request = $.ajax({
            url: MODULEURL + mhashid,

        xhrFields: {
            withCredentials: true
        },
            type: 'GET'
        });

        request.done(function(data) {
            //why not returned as json???
            var jdata = $.parseJSON(data);
            alert("sending jdata" + jdata);
            logout(jdata);
            //weird aloha feature - suffixed textareas.. ask phil..
            $('#editarea-aloha').val(jdata['content']);
            $('#aclrw').val(jdata['aclrw']);
            $('#contentrw').val(jdata['contentrw']);
            $('#title').val(jdata['title']);
            $('#uuid').val(jdata['uuid']);

        });

        request.fail(function(jqXHR, textStatus, err) {
            logout('Request failed: ' + textStatus + ':' + err + ':' + jqXHR.status);
        });

        request.always(function(jqXHR, textStatus) {
            logout(textStatus);
        });
    }


function getLoadHistoryVer(uuid) {
    // ajax request to retrieve module and parse json and load into textarea
    $.ajax({
        type: 'GET',
        dataType: 'json',
        url: MODULEURL + uuid,
        xhrFields: {
            withCredentials: true
        },  //http://stackoverflow.com/questions/2870371/why-jquery-ajax-not-sending-session-cookie


        success: function(nodedoc) {
            var title = nodedoc['title'];
            var txtarea = nodedoc['content'];

            var aclrw = nodedoc['aclrw'];
            var contentrw = nodedoc['contentrw'];

            $('#title').val(title);
            $('#aclrw').val(aclrw);
            $('#contentrw').val(contentrw);
            $('#uuid').val(uuid);

            $('#editarea-aloha').html(txtarea);
        },

        error: function(jqXHR, textStatus, err) {
            logout('Request failed: ' + textStatus + ':' + err + ':' + jqXHR.status);
        },

        complete: function(jqXHR, textStatus, err) {
            logout('Complete: Request failed: ' + textStatus + ':' + err + ':' + jqXHR.status);
        }


    });
}


function getwhoami() {
    // ajax request
    $.ajax({
        type: 'GET',
        dataType: 'json',
        url: REPOBASEURL + '/whoami/',
        xhrFields: {
            withCredentials: true
        },
        //display who I am
        success: function(jsondoc) {

//            for (var i in jsondoc){
//               alert(i);
//            };
            var user_email = jsondoc['email'];
            var user_name = jsondoc['name'];
            $('#usernamedisplay').html(user_name + '-' + user_email);
        },

        error: function(jqXHR, textStatus, err) {
            logout('Request failed: ' + textStatus + ':' + err + ':' + jqXHR.status);
        }

    });
}




function build_workspace() {

    logout("In build workspace");
    var jsond = '[';
    var htmlfrag = '<ul>';
    $.ajax({
        type: 'GET',
        dataType: 'json',
        url: WORKSPACEURL,
        xhrFields: {
            withCredentials: true
        },  //http://stackoverflow.com/questions/2870371/why-jquery-ajax-not-sending-session-cookie

        success: function(historyarr) {
            historyarr.sort();
            if (historyarr.length == 0){
                alert("No workspace to deal with");
                                      }
            else {

                $.each(historyarr, function(i, elem) {
                    var strelem = "'" + elem[0] + "'";
                    htmlfrag += '<li><a class="nolink" href="#" onclick="getLoadHistoryVer(' + strelem + ');" >' + elem[1] + '</a>' + '<a class="nolink" href="#" onclick="delete_module(' + strelem + ');" >(Delete)</a>';
                    jsond += '{"data": "' + elem[1] + '", "attr": {"id": "' + elem[0] + '"}, "state": "closed"},';
                });


                x = jsond.length - 1;
                y = jsond.substring(0, x);
                jsond = y + ']';
                //jsond += ']"';
                logout("Building workspace :" + htmlfrag);
                logout(jsond);
                $('#workspaces').html(htmlfrag);
            }
        }
    });
}

function delete_module(filename) {
    $.ajax({
        type: 'DELETE',
        dataType: 'json',
        url: REPOBASEURL + '/module/' + filename,
        xhrFields: {
            withCredentials: true
        },  //http://stackoverflow.com/questions/2870371/why-jquery-ajax-not-sending-session-cookie

        success: function() {
            logout('deleted ' + filename);
            build_workspace();
        },

        error: function(jqXHR, textStatus, err) {
            logout('Request failed: ' + textStatus + ':' + err + ':' + jqXHR.status);
        }

    });

}

function showres(i, elem) {

    logout(i + ': ' + elem);
}


function serialise_form() {
    // return form1 as object/hasharrary
    var payload = new Object;
    payload['content'] = get_textarea_html5();
    payload['uuid'] = $('#uuid').val();

    payload['aclrw'] = $('#aclrw').val().split(',');

    payload['contentrw'] = $('#contentrw').val().split(',');
    payload['title'] = $('#title').val();

//        var json_text = JSON.stringify(payload, null, 2);
//        return json_text;

    return payload;

}

function newText() {
    $('#aclrw').val(whoami['userID']);
    $('#contentrw').val(whoami['userID']);
    $('#title').val('Enter title here ...');
    $('#uuid').val('');
    $('#editarea-aloha').html('Enter your text here...');


}

function saveText() {
         //constants

         if (save_validate() == false) {
             alert("I should stop saving now");
         };

         var requestmethod = 'POST';
         var payload = serialise_form();
         if (payload['uuid'] != '') {
             requestmethod = 'PUT';
         }

         var foo = '';
         for (var i in payload) {
             foo = '/n' + i + ' : ' + payload[i];
         }
//         alert(requestmethod);
//         alert(foo);

         var json_text = JSON.stringify(payload, null, 2);

         var request = $.ajax({
             url: MODULEURL,
                xhrFields: {
                 withCredentials: true
                },


             type: requestmethod,
             data: json_text,
             contentType: 'application/json; charset=utf-8',
             dataType: 'json'
         });

         request.done(function(data) {
             //$("#responsearea").html(data);
             $.each(data, showres);
             build_workspace();
         });

         request.fail(function(jqXHR, textStatus, err) {
             logout('Request failed: ' + textStatus + ':' + err + ':' + jqXHR.status);
         });

         request.always(function(jqXHR, textStatus) {
             logout(textStatus);
         });

    }

function start_aloha() {

    $('#editarea').aloha();
    logout('started aloha');
}

function node_load_event(node) {


   var moduleuuid = node.attr('id');
   getLoadHistoryVer(moduleuuid);
//   var s = "Calling load_textarea(" + moduleuuid + ")";
//   logout(s);
//   load_textarea(moduleuuid);

   }

////////////////////// Persona

function persona_in(){
   alert("persona in clicked");
   navigator.id.request();

}


function persona_out(){
   alert("persona out clicked");
   navigator.id.logout();

}



////////////// adminy
function test(){
    build_workspace();
    alert("start aloha now ..");
//    phil_aloha_start();
    start_aloha();
}




$(document).ready(function() {
//$(window).load(function() {

    //start_aloha();
    //phil_aloha_start();

    //bind various clicks - clearly refactorable
    $('#testbtn').click(function(e) {test();
                                      e.preventDefault()});

    $('#persona_signin').click(function(e) {persona_in();
                                            e.preventDefault()
                                           });

    $('#persona_signout').click(function(e) {persona_out();
                                      e.preventDefault()});


    $('#clickLoadTextArea').click(function(e) {load_textarea();
                                              e.preventDefault()});


    $('#savemodule').click(function(event) {
                         saveText();
                         event.preventDefault();
                       }
                      );

    $('#newmodule').click(function(event) {
                         newText();
                         event.preventDefault();
                       }
                      );

    //nolink are links that do some jquery function, but should not be links
    $('a.nolink').click(function(event) {
        event.preventDefault();
     });


//    getwhomi();



    build_workspace();


    /* Authoring Tools Dropdowns & Modals */
    Tools.construct()
    /* END Authoring Tools Dropdowns & Modals */

navigator.id.watch({
  loggedInUser: whoami['authenticated_identifier'],
  onlogin: function(assertion) {
    // A user has logged in! Here you need to:
    // 1. Send the assertion to your backend for verification and to create a session.
    // 2. Update your UI.
    $.ajax({
      type: 'POST',
      url: PERSONAURL,
      data: {assertion: assertion},
      success: function(res, status, xhr) { alert("login success on server" + res); },
      error: function(res, status, xhr) { alert("login failure" + res); }
    });
  },

  onlogout: function() {
    // A user has logged out! Here you need to:
    // Tear down the user's session by redirecting the user or making a call to your backend.
    //window.location = 'google.com';
    $.ajax({
      type: 'POST',
      url: PERSONALOGOUT,
      success: function(res, status, xhr) { alert("You whosul be logged out with reload"); },
      error: function(res, status, xhr) { alert("logout failure" + res); }
    });
  }
});




});
