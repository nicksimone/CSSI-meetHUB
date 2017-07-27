console.log("Yo");

function write_user_name () {
  var user_name = $("#name_box").val();
  $("#posts").text(user_name);
}
function setUp() {
  $("#button_ok").click(write_user_name);
  $("#button_join").click(addAttending);
  // $('#search_button_ok').click()
}
// var number_attending = 0;
// function addAttending() {
//   global number_attending;
//   number_attending += 1;
// }
$(document).ready(setUp);
