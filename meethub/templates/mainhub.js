console.log("Yo");
function write_user_name () {
  var user_name = $("#name_box").val();
  $("#posts").text(user_name);
}
function setUp() {
  $("#button_ok").click(write_user_name);
}

$(document).ready(setUp);
