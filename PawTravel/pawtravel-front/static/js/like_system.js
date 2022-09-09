// get csrf token
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

/*
The functions below will create a header with csrftoken
*/

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}
// ======================================================================================================================
//like function
$(function() {
    $(document).on('click', '.likes', function() {
            var object_id = $(this).data('id')
            var action_type = $(this).data('type')
            var likesystem_block = $(this).closest('.likesystem')

            $.ajax({
                url : '/'+action_type+'/'+ object_id +'/like',
                context: $(likesystem_block),
                type : 'POST',


                success : function(data) {
                    if (data) {
                        $(likesystem_block).find('.countlikes').text(data.likes);
                        $(likesystem_block).find('.countdislikes').text(data.num_votes);
                    }
                },

                error : function(xhr,errmsg,err) {
                    console.log(xhr.status+': '+xhr.responseText);
                },
            });
    });

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});



// ======================================================================================================================
//dislike function
$(function() {
    $(document).on('click', '.dislikes', function() {
            var object_id = $(this).data('id')
            var action_type = $(this).data('type')

            $.ajax({
                url : '/'+action_type+'/'+ object_id +'/dislike',
                context: $(this),
                type : 'POST',

                success : function(data) {
                    if (data) {
                        $(this).parents('.likesystem').find('.countlikes').text(data.likes);
                        $(this).siblings('.countdislikes').text(data.num_votes);
                    }
                    //console.log(data);
                },

                error : function(xhr,errmsg,err) {
                    console.log(xhr.status+': '+xhr.responseText);
                    $('#exampleModalCenter').modal('show');
                },
            });
    });

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});