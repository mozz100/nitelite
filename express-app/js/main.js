var client = new Faye.Client('/');

client.subscribe('/state', function(data) {
  alert('data: ' + data.state);
});

// intercept form POSTs and do with AJAX
$('form').submit(function(e) {
    var frm = $(this);
    e.preventDefault();
    $.post(frm.attr('action'), frm.serialize());
});