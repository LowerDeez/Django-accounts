$(document).ready(function() {
  //автоматическое исчезновение уведомления при смене пароля
  $(".alert").delay(4000).slideUp(200, function() {
      $(this).alert('close');
  });

});
