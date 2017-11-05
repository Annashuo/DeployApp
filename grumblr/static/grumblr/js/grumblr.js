
function getUpdates() {
  console.log("update");
    var list = $("#allpost")
    var max_time = $(".time")[0].id;
    console.log(max_time);
    $.get("/get-changes/"+max_time)
      .done(function(data) {
          //list.data('max-time', data['max-time']);
          for (var i = 0; i < data.items.length; i++) {
              var item = data.items[i];
              var new_item = $(item.html);
              //new_item.data("item-id", item.id);
              list.prepend(new_item);
          }
      });
}
function addComment(e){
  var id = $(e.target).parent().parent().parent()[0].id;
  var commentinput = $(e.target).prev();
  console.log(id);
  if(commentinput.val() != ''){
    $.post("/addcomment/"+id+"/",{"comment":commentinput.val()})
      .done(function(data){
        var commentplace = $(e.target).parent().parent()
        console.log(commentplace);
        console.log(commentplace.data('max-time'));
        $.get("/comment/"+id, {'time': commentplace.data('max-time')})
          .done(function(data){
            commentplace.data('max-time', data['max-time']);
            for (var i = 0; i < data.items.length; i++) {
                item = data.items[i];
                var new_item = $(item.html);
                commentplace.append(new_item);
            }
        });
        var max_time = $(".time")[0].id;
        if(max_time!=''){
          getUpdates();
        }
        commentinput.val("").focus();
      });
  }

}

function showComment(e) {
  var commentplace = $(e.target).parent().next();
  var list = $(e.target).parent().next().children(); 
  if (list.length != 0){
    commentplace.empty();
    return;
  }
  var div = document.createElement("div");
  var input = document.createElement("textarea");
  var button = document.createElement("button");
  div.style = "margin-bottom:10px;";
  input.rows = "1";
  input.style = "width:60%; margin:0 10px 0 20px;";
  button.id = "addcomment";
  button.className = "btn btn-default";
  button.innerText = "add comment";
  div.appendChild(input);
  div.appendChild(button);
  commentplace.append(div); //appendChild

  var id = $(e.target).parent().parent()[0].id;

  $.get("/comment/"+id)
    .done(function(data){
      commentplace.data('max-time', data['max-time']);
      for (var i = 0; i < data.items.length; i++) {
          item = data.items[i];
          var new_item = $(item.html);
          commentplace.append(new_item);
      }
    });
  //e.preventDefault();
}


$(document).ready(function () {
  // Set up to-do list with initial DB items and DOM data
  $("#allpost").on( "click", "#comment", showComment);
  $("#allpost").on( "click", '#addcomment', addComment);
  var max_time = $(".time")[0].id;
  if(max_time!=''){
    window.setInterval(getUpdates, 5000);
  }
  // CSRF set-up copied from Django docs

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
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  });
});