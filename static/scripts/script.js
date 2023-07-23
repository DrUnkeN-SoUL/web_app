$(document).ready(function () {
  $('input.slider').click(function () {
    // Toggle 'dark' class on the body element
    $('body').toggleClass('dark');
});

  $(".btn-close-right").click(function () {
    $(".right-side").removeClass("show");
    $(".expand-btn").addClass("show");
  });

  $(".expand-btn").click(function () {
    $(".right-side").addClass("show");
    $(this).removeClass("show");
  });
});