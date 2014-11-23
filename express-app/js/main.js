var client = new Faye.Client('/faye');
client.disable('websocket');

client.subscribe('/state', function(data) {
  alert('data: ' + data.state);
});

// intercept form POSTs and do with AJAX
$('input[type="submit"], button[type="submit"]').click(function(e) {
    var frm = $('form');
    e.preventDefault();
    var btn = $(e.delegateTarget);
    $.post(frm.attr('action'), btn.attr('name')+'='+btn.attr('value'));
});
