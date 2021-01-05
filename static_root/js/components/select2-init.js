//Title:demo for select2 element
//Author:www.madcoderz.com
//madol
$(function () {
    'use strict';
    //basic select
    $('.js-example-basic-single').select2();
    //multiple select
    $('.js-example-basic-multiple').select2();
    //theme
    $(".js-example-theme-single").select2({
        theme: "classic"
    });
    //example theme multiple 
    $(".js-example-theme-multiple").select2({
        theme: "classic"
    });

    function formatState(state) {
        if (!state.id) {
            return state.text;
        }
        var baseUrl = "http://www.madcoderz.com/madol/asset/images/flags";
        var $state = $(
            '<span><img src="' + baseUrl + '/' + state.element.value.toLowerCase() + '.png" class="img-flag" /> ' + state.text + '</span>'
        );
        return $state;
    };
    //placeholder option
    $(".js-example-placeholder-single").select2({
        placeholder: "Select a state",
        allowClear: true
    });
    //country id and name
    //search minimum 2 value
    $(".example-minimum-input").select2({
        minimumInputLength: 2,
        placeholder: "Select a State",
    });
});