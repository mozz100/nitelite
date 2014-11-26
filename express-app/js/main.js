var client = new Faye.Client('/faye');

client.subscribe('/state', function(data) {
  showState(data.state);
});

client.subscribe('/times', function(data) {
  showTimes(data);
});

// intercept form POSTs and do with AJAX
$('#state input[type="submit"], #state button[type="submit"]').click(function(e) {
    var frm = $('form#state');
    e.preventDefault();
    var btn = $(e.delegateTarget);
    $.post(frm.attr('action'), btn.attr('name')+'='+btn.attr('value'));
});
$('#times input').change(function(e) {
    var frm = $('form#times');
    e.preventDefault();
    $.post(frm.attr('action'), frm.serialize());
});

function showState(state) {
    $('.btn').removeClass('btn-current');
    $('.btn[value="' + state + '"]').addClass('btn-current');
}
function showTimes(data) {
    $('#nitetime').val(data.nitetime);
    $('#litetime').val(data.litetime);
    $('#offtime').val(data.offtime);
}

// get initial state and times
$.get('/state', function(data) {
   showState(data.state);
});
$.get('/times', function(data) {
   showTimes(data);
});
