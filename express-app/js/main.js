var client = new Faye.Client('/faye');

client.subscribe('/state', function(data) {
  showState(data.state);
});

// intercept form POSTs and do with AJAX
$('input[type="submit"], button[type="submit"]').click(function(e) {
    var frm = $('form');
    e.preventDefault();
    var btn = $(e.delegateTarget);
    $.post(frm.attr('action'), btn.attr('name')+'='+btn.attr('value'));
});

function showState(state) {
    $('.btn').removeClass('btn-current');
    $('.btn[value="' + state + '"]').addClass('btn-current');
}

// get initial state
$.get('/state', function(data) {
   showState(data.state);
});
