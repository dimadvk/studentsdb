function initJournal() {
    var indicator = $('#ajax-progress-indicator');

    $('.day-box input[type="checkbox"]').click(function(event){
        var box = $(this);
        $.ajax(box.data('url'), {
            'type': 'POST',
            'async': true,
            'dataType': 'json',
            'data': {
                'pk': box.data('student-id'),
                'date': box.data('date'),
                'present': box.is(':checked') ? '1': '',
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            'beforeSend': function(xhr, settings){
                indicator.show();
            },
            'error': function(xhr, status, error){
                $('#ajax-error').show();
                $('#ajax-error-text').text("ERROR: Data not saved. " + error);
                indicator.hide();
            },
            'success': function(data, status, xhr){
                indicator.hide();
            }
        });
    });
}

function initGroupSelector(){
    // look up select element with groups and attach our even handler
    // on field "change" event
    $('#group-selector select').change(function(event){
        var group = $(this).val();

        if (group) {
            // set cookie with expiration date 1 year since now;
            // cookie creation function takes period in days
            $.cookie('current_group', group, {'path': '/', 'expires': 365});
        } else {
            // otherwise we delete the cookie
            $.removeCookie('current_group', {'path': '/'});
        }

        // and reload a page
        // location.reload(true);
        location = '/' + location.pathname.split('/')[1];

        return true;
    });
}

function initDateFields() {
    $('input.dateinput').datetimepicker({
        format: 'YYYY-MM-DD',
        locale: 'uk'
    }).on('dp.hide', function(event){
        $(this).blur();
    });
    var datefield = $('#div_id_birthday div');
    datefield.find('input').attr('aria-describedby', 'calendar-icon');
    datefield.append('<span class="input-group-addon">'
            + '<i class="glyphicon glyphicon-calendar"'
            + 'id="calendar-addon" aria-hidden="true"></i></span>');
    datefield.wrapInner('<div class="input-group"> </div>');
}

function renewStudentsList(data, student_id) {
    $('table #'+student_id).html($(data).find('table #'+student_id).html());
}

function initEditStudentForm(form, modal) {
    // attache datepicker
    initDateFields();
    initPhotoField();

    // close modal window on Cancel button click
    form.find('input[name="cancel_button"]').click(function(event){
        modal.modal('hide');
        return false;
    });

    // make form work in AJAX mode
    form.ajaxForm({
        'dataType': 'html',
        'error': function(){
            //alert('Помилка на сервері. Спробуйте будь-ласка пізніше. form.ajaxForm()');
            $('#modal-message-block').show();
            $('#modal-message').html('<b>Error:</b> Помилка на сервері. Спробуйте будь-ласка пізніше.');
            return false;
        },
        'success': function(data, status, xhr) {
            var html = $(data), newform = html.find('#content-column form.form-horizontal');

            // copy alert to modal window
            modal.find('.modal-body').html(html.find('.alert'));

            $('#modal-message-block').hide();

            // copy form to modal if we found it in server response
            if (newform.length > 0) {
                modal.find('.modal-body').append(newform);

                // initialize form fields and buttons
                initEditStudentForm(newform, modal);
            } else {
                // if no form, it means success and we need to reload page
                // to get updated student list;
                // reload after 2 seconds, so that user can read
                // success message
                //setTimeout(function(){location.reload(true);}, 500);
                student_id = $(form).attr('action').split('/')[2];
                $('table #'+student_id).html(
                    $(data).find('table #'+student_id).html()
                );
                initEditStudentPage();
            }
        },
        'beforeSend': function() {
            $('.ajax-loader-modal img').show();
            $('input, select, textarea, a, button').attr('disabled', 'disabled');
        },
        'complete': function() {
            $('.ajax-loader-modal img').hide();
            $('input, select, textarea, a, button').removeAttr('disabled', 'disabled');
        }
    });
}

function initEditStudentPage() {
    $('a.student-edit-form-link').click(function(event){
       // // dvk: find all anchors with a class .student-edit-form-link
       // var studentEditAnchors = $('a.student-edit-form-link');
       // $('a').click(function (event) {
       //     event.preventDefault();
       // });
        
        var link = $(this);
        $.ajax({
            'url': link.attr('href'),
            'dataType': 'html',
            'type': 'get',
            'success': function(data, status, xhr){
                // check if we got successfull response from the server
                if (status != 'success') {
                    alert('Помилка на сервері. Спробуйте пізніше.');
                    return false;
                }

                // update modal window with arrived content from the server
                var modal = $('#myModal');
                html = $(data), form = html.find('#content-column form');
                modal.find('.modal-title').html(html.find('#content-column h2').text());
                modal.find('.modal-body').html(form);

                // init our edit form
                initEditStudentForm(form, modal);
                

                // setup and show modal window finally
                modal.modal({
                    'keyboard': false,
                    'backdrop': false,
                    'show': true
                });
            },
            'error': function(){
                alert('Помилка на сервері. Спробуйте будь-ласка пізніше.');
                return false;
            },
            'beforeSend': function() {
                $('.ajax-loader').show();
            },
            'complete': function() {
                $('.ajax-loader').hide();
            }
        });
        return false;
    });
}

function navTabs() {
    var navLinks = $('.nav-tabs li > a');
    navLinks.click(function(event) {
        var url = this.href;
        $.ajax({
            'url': url,
            'dataType': 'html',
            'type': 'get',
            'success': function(data, status, xhr){
                // check if we got successful responcse
                if (status != 'success') {
                    alert('Помилка на сервері.');
                    return false;
                };
                
                // update table
                var content = $(data).find('#content-columns');
                var pageTitle = content.find('h2').text();
                $(document).find('#content-columns').html(content.html());
                navLinks.each(function(index){
                    if (this.href === url) {
                      $(this).parent().addClass('active');
                    } else {
                      $(this).parent().removeClass('active');
                    };
                });
                // update uri in address bar
                window.history.pushState("string", pageTitle, url);
                // update page title
                document.title = $(data).filter('title').text();
            },
            'error': function() {
                alert('Помилка на сервері.');
                return false;
            },
            'beforeSend': function() {
                $('.ajax-loader').show();
            },
            'complete': function() {
                $('.ajax-loader').hide();
                initFunctions();
            }
        });
        event.preventDefault();
    });
}

function closeModalBackButton() {
    window.addEventListener('popstate', function() {
        $('#myModal').modal('hide');
        window.history.pushState("string", '', '/');
    });
}

function initPhotoField(){
    var imgUrl = $('#div_id_photo a').attr('href');
    var imgHtml = '<img heigh="30" width="30" class=img-circle src=' +  imgUrl + '/>'
    $('#div_id_photo a').html(imgHtml);
}

//
//function initPhotoFieldWidget(){
//    var imgUrl = $('#div_id_photo a').attr('href');
//    $('#div_id_photo div.controls').html('<div id="fileuploader">Upload</div>');
//    uploadImgWidget();
//}
//
//function uploadImgWidget() {
//    $("#fileuploader").uploadFile({
//    url:"{% url 'test2' %}",
//    fileName:"photo",
//    multiple: false,
//    dragDrop: true,
//    maxFileCount:1,
//    acceptFiles:"image/*",
//    maxFileSize:2*1024*1024,
//    showPreview:true,
//      previewHeight: "35px",
//      previewWidth: "35px",
//    showDelete: true,
//    autoSubmit: false,
//    dragdropWidth:245,
//    statusBarWidth:245,
//    dragDropStr: "<span style='font-size:0.9em; display:inline-block; margin-top:0px; margin-left:20px;'><b>Перетягніть<br> сюди фото</b></span>",
//    extErrorStr:"Файл не є зображенням.",
//    sizeErrorStr:"Завеликий файл, має бути менше: ",
//    uploadStr:"Завантажити"
//    });
//}


$(document).ready(initFunctions);
function initFunctions(){
    initJournal();
    initGroupSelector();
    initDateFields();
    initEditStudentPage();
    navTabs();
    closeModalBackButton();
}
