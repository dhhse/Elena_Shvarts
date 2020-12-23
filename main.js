


var links = document.getElementsByClassName('changeable');
function changeColor(e) {
    e.target.style.color = e.target.style.color ? null : 'black';
}
for (var i = 0; i < links.length; i++) {
    links[i].addEventListener('click', changeColor);
}

$(function() {
  $('a#process_input').bind('click', function() {
    $.getJSON('/background_process', {
      search: $('input[name="search"]').val(),
      }, function(data) {
              $("ul").empty();
              $(data.result).each(function (index, value) {
                $("ul").append('<li class="for_search"><a class="for_search" href="../texts_60_' +
                      value[0] + '/">' + 
                    value[1] + '</a></li>');
          });
        });
        return false;
        });
      });