// Functions for setting the UI state and timer values.
function showState(data) {
    // clear the btn-current class from all buttons except one
    $('.btn').removeClass('btn-current');
    $('.btn[value="' + data.state + '"]').addClass('btn-current');
}
function showTimes(data) {
    // Take the three times and put them into the corresponding <input> elements
    $.each(['nitetime', 'litetime', 'offtime'], function(index, prop) {
        $('input#' + prop).val(data['prop']);
    })
}

// Set up Faye client and listen for state and timer changes
var client = new Faye.Client('/faye');
client.subscribe('/state', showState);
client.subscribe('/times', showTimes);

// Make a GET request to fetch initial state and times
$.get('/state', showState);
$.get('/times', showTimes);

// For state changes, intercept button presses and do form submit with AJAX
$('#state button[type="submit"]').click(function(e) {
    var frm = $('form#state');
    e.preventDefault();
    var btn = $(e.delegateTarget);
    $.post(frm.attr('action'), btn.attr('name')+'='+btn.attr('value'));
});
// For timers, listen for change and POST the form.
$('#times input').change(function(e) {
    var frm = $('form#times');
    e.preventDefault();
    $.post(frm.attr('action'), frm.serialize());
});

