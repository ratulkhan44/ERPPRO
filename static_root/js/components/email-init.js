$(function(){


    // Mail compose
    var quill = new Quill('#compose-mail', {
      modules: {
        toolbar: '#toolbar-container'
      },
      placeholder: 'Write your message here...',
      theme: 'snow'
    });




    // $('.mail-options-dropdown').click(function(e){
    //
    //   e.stopPropagation();
    //   e.preventDefault();
    //   // $(this).children('.dropdown-menu').toggleClass('show');
    //   $('.mail-options-dropdown .dropdown-toggle').dropdown('toggle');
    //   console.log($(this).find('.dropdown-toggle'));
    //
    // });



    // $(this).attr('class').split(' ')[0];
    // $('.dropdown-toggle').dropdown()
    //if ($('.mail-options-dropdown').find('.dropdown-menu').is(":hidden")){
      // $(this).find('.dropdown-toggle').dropdown();
      // if($(e.target).attr('class').split(' ')[0] == 'mail-options-dropdown' ) {
        //   $(this).children('.dropdown-menu').toggleClass('show');
        // } else {
          //   $(this).children('.dropdown-menu').removeClass('show');
          // }
          //}

    // $(".mail-options-dropdown").click(function(ev) {
    //   $(".mail-options-dropdown.dropdown-toggle").dropdown("toggle");
    //   return false;
    // });

    

});
