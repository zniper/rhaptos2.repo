// Copyright (c) Rice University 2012
// This software is subject to
// the provisions of the GNU Lesser General
// Public License Version 2.1 (LGPL).
// See LICENCE.txt for details.
//


// Notes
// This file is the (messy) beginings of Author TOols on browseer
// It will supply an API for _editor_ to use,
// It will commiunicate with the unpub repo and user profile server
// it will make tea


// ..todo:: Persona fires through navigator.id.watch at odd times on start up

// pick up some constants, from constants file

    var REPOBASEURL = 'http://' + FROZONE.e2repoFQDN;
    var MODULEURL = 'http://' + FROZONE.e2repoFQDN + '/module/';
    var WORKSPACEURL = 'http://' + FROZONE.e2repoFQDN + '/workspace/';

    var PERSONAURL = 'http://' + FROZONE.e2repoFQDN + '/persona/login/';
    var PERSONALOGOUT = 'http://' + FROZONE.e2repoFQDN + '/persona/logout/';



    function logger(msg) {
        //log both to console and to web page,
        //splitting out objects as we go for visibility
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

// Pull-only commands to interact with the editor area
// I mean pull only to mean treat ediotor as black box and do things to it, not
// as I would like where eventually ediotor supplies an API

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
        var txtarea = $('#editarea').html();
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
            logger(jdata);
            //weird aloha feature - suffixed textareas.. ask phil..
            $('#editarea').val(jdata['content']);
            $('#aclrw').val(jdata['aclrw']);
            $('#contentrw').val(jdata['contentrw']);
            $('#title').val(jdata['title']);
            $('#uuid').val(jdata['uuid']);

        });

        request.fail(function(jqXHR, textStatus, err) {
            logger('Request failed: ' + textStatus + ':' + err + ':' + jqXHR.status);
        });

        request.always(function(jqXHR, textStatus) {
            logger(textStatus);
        });
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
    $('#editarea').html('Enter your text here...');


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
             // Put the UUID in the form field.
             $('#uuid').val(data.hashid);
             build_workspace();
         });

         request.fail(function(jqXHR, textStatus, err) {
             logger('Request failed: ' + textStatus + ':' + err + ':' + jqXHR.status);
         });

         request.always(function(jqXHR, textStatus) {
             logger(textStatus);
         });

    }


// FUnctions to get worksapce and display it

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

            $('#editarea').html(txtarea);
        },

        error: function(jqXHR, textStatus, err) {
            logger('Request failed: ' + textStatus + ':' + err + ':' + jqXHR.status);
        },

        complete: function(jqXHR, textStatus, err) {
            logger('Complete: Request failed: ' + textStatus + ':' + err + ':' + jqXHR.status);
        }


    });
}




function build_workspace() {

    logger("In build workspace");
    var jsond = '[';
    var htmlfrag = '<table class="table table-condensed table-hover table-striped" >';
    $.ajax({
        type: 'GET',
        dataType: 'json',
        url: WORKSPACEURL,
        xhrFields: {
            withCredentials: true
        },  
        success: function(historyarr) {
            historyarr.sort();
            if (historyarr.length == 0){
                logger("Not logged in - no workspace to deal with");
                                      }
            else {

                $.each(historyarr, function(i, elem) {
                    var strelem = "'" + elem[0] + "'";
                      
                    htmlfrag += '<tr><td><a class="nolink" href="#" onclick="getLoadHistoryVer(' + strelem + ');" >' + elem[1] + '</a></td>' + '<td><a class="nolink" href="#" onclick="delete_module(' + strelem + ');" >(Delete)</a></td></tr>';
                    jsond += '{"data": "' + elem[1] + '", "attr": {"id": "' + elem[0] + '"}, "state": "closed"},';
                });


                x = jsond.length - 1;
                y = jsond.substring(0, x);
                jsond = y + ']';
                //jsond += ']"';
                logger("Building workspace :" + htmlfrag);
                logger(jsond);
                $('#workspaces').html(htmlfrag);
            }
        }
    });
}


// We are changing how identiy is managed - and need beter secure coiokies

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
            logger('Request failed: ' + textStatus + ':' + err + ':' + jqXHR.status);
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
            logger('deleted ' + filename);
            build_workspace();
        },

        error: function(jqXHR, textStatus, err) {
            logger('Request failed: ' + textStatus + ':' + err + ':' + jqXHR.status);
        }

    });

}

function showres(i, elem) {

    logger(i + ': ' + elem);
}

/////////////// Aloha

function start_aloha() {

    $('#editarea').aloha();
    logger('started aloha');
}

function node_load_event(node) {


   var moduleuuid = node.attr('id');
   getLoadHistoryVer(moduleuuid);
//   var s = "Calling load_textarea(" + moduleuuid + ")";
//   logger(s);
//   load_textarea(moduleuuid);

   }

////////////////////// Persona

function persona_in(){
   logger("persona in clicked");
   navigator.id.request();

}


function persona_out(){
   logger("persona out clicked");
   navigator.id.logout();

}



////////////// adminy
function test(){
    build_workspace();
    logger("start aloha now ..");
    start_aloha();

}




$(document).ready(function() {
//$(window).load(function() {

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


    newText();
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
      success: function(res, status, xhr) { console.log("login success on server" + res); },
      error: function(res, status, xhr) { console.log("login failure" + res); }
    });
  },

  onlogout: function() {
    // A user has logged out! Here you need to:
    // Tear down the user's session by redirecting the user or making a call to your backend.
    //window.location = 'google.com';
    $.ajax({
      type: 'POST',
      url: PERSONALOGOUT,
      success: function(res, status, xhr) { console.log("You whosul be logged out with reload"); },
      error: function(res, status, xhr) { console.log("logout failure" + res); }
    });
  }
});




});


Aloha.ready( function() {
    Aloha.jQuery('.document').aloha();
      // Wait until Aloha is started before loading MathJax

      // pbrian - not clear how to start MathJax...

      // Also, wrap all math in a span/div. MathJax replaces the MathJax element
      // losing all jQuery data attached to it (like popover data, the original Math Formula, etc)
//      $('math').wrap('<span class="math-element"></span>')
//      MathJax.Hub.Configured();
      //$('*[rel=tooltip]').tooltip();
});