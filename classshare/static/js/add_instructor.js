$(document).ready(function() {
    instructor_select = $('#id_instructor');
    instructor_text = $('<input type="text" placeholder="First Last" name="instructor" id="id_instructor" />');
    add_icon = $('#add-instructor img');
    remove_icon = $('<img src="'+ STATIC_PREFIX +'img/icon_deletelink.gif" title="Cancel" alt="Cancel Add Instructor"/>');
    $('#add-instructor').click(function() {
	if ($(this).hasClass('add-another')) {
	    $('#id_instructor').replaceWith(instructor_text);
	    $(this).find('img').replaceWith(remove_icon);
	    $('#new-instructor').attr('value', 'True');
	}
	else {
	    $('#id_instructor').replaceWith(instructor_select);
	    $(this).find('img').replaceWith(add_icon);
	    $('#new-instructor').attr('value', 'False');
	}
	$(this).toggleClass('add-another remove-another');
    });
});