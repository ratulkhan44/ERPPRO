$(function() {
    $('[data-toggle="popover"]').popover();
});

$(function() {
    $('[data-toggle="tooltip"]').tooltip();
});

$(function() {
    "use strict";
    $("#preview_image").on("change", function() {
        var a = $(".image-preview");
        this.files && $.each(this.files, function(e, i) {
            if (!/\.(jpe?g|png|gif)$/i.test(i.name)) return alert(i.name + " is not an image");
            var l = new FileReader;
            $(l).on("load", function() {
                a.append("<span class='upload-wrapper'><span class='upload-wrapper-delete'>X</span><img src='" + this.result + "'></span>")
            }), l.readAsDataURL(i), $(document).on("click", ".upload-wrapper-delete", function(a) {
                $(this).parents(".upload-wrapper").remove(), $(this).remove()
            })
        })
    });

});

$('#searchIcon').on('click', function(e) {
  e.preventDefault();
  $('.search-input-field').addClass('show');
  $('.shade').addClass('visible');
});

$('#closeSearchBox').on('click', function(e) {
  e.preventDefault();
  $('.search-input-field').removeClass('show');
  $('.shade').removeClass('visible');
});

var ps = new PerfectScrollbar('.aside-inner', {
  suppressScrollX: true,
  wheelPropagation:false
});

var ps2 = new PerfectScrollbar('.notification-wrapper', {
  suppressScrollX: true,
  wheelPropagation:false
});

// Sidemenu scripts
$('.has-submenu > a').on('click', function(e) {
  e.preventDefault();
  $(this).closest('.has-submenu').toggleClass('drop-down');
});

$('body').on('mouseenter', '.aside-wrapper.aside-minimized', function(e) {
  $(this).addClass('aside-display-full');
});

$('body').on('mouseleave', '.aside-wrapper.aside-minimized', function(e) {
  $(this).removeClass('aside-display-full');
  ps.update();
});


/* JavaScript Media Queries */
if (matchMedia) {
  var mq = window.matchMedia("(min-width:992px) and (max-width: 1199px)");
  mq.addListener(activateMiniSidebar);
  activateMiniSidebar(mq);
}

function activateMiniSidebar(mq) {
  if (mq.matches) {
    $(".aside-wrapper").addClass("aside-minimized");
  } else {
    $(".aside-wrapper").removeClass("aside-minimized");
  }
  ps.update();
}

$(".switch-sidebar-mode").on("click", function(e){
  e.preventDefault();
  if(window.matchMedia("(min-width: 992px)").matches) {
    $(".aside-wrapper").toggleClass("aside-minimized");
    console.log('here');
  }
  ps.update();
});

$(".switch-sidebar-mode").on("click", function(e){
  e.preventDefault();
  if(window.matchMedia("(max-width: 991px)").matches) {
      $("#app").toggleClass("aside-display");
      console.log('here');
  }
  ps.update();
});


//Bootstrap upload file-name fix


$('input[type="file"]').change(function(e){
  var fileName = e.target.files[0].name;
  $('.custom-file-label').html(fileName);
});
