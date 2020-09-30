$(function() {
    'use strict';
            //initiate the plugin and pass the id of the div containing gallery images
        $("#zoom_03").elevateZoom({
            zoomType: 'lens',
            lensShape: 'square',
            lensSize: '250',
            easing: true,
            cursor: 'pointer',
            galleryActiveClass: 'active',
            zoomWindowPosition: 11,
            gallery: 'gallery_01',
            borderSize: 0,
            containLensZoom: true,
            responsive: true,
            lensShape: 'round'
        });

        //pass the images to Fancybox
        $("#zoom_03").bind("click", function(e) {
            $('#zoom_03').data('elevateZoom');
            return false;
        });
        $(".switch-label").on("click", function() {
            $("#product_color")
                .val($(this).data("value"))
                .trigger("change");
            $(this).addClass("selected");
            $(this)
                .siblings()
                .removeClass("selected");
            $("#product_size")
                .val($(this).data("value"))
                .trigger("change");
            $(this).addClass("selected");
            $(this)
                .siblings()
                .removeClass("selected");
        });
});