$(function () {
    "use strict";

    $(document).ready(function () {
        var form = $("#vertical-wizard").show();
        form.steps({
            headerTag: "h3",
            bodyTag: "section",
            autoFocus: true,
            titleTemplate: '<span class="number">#index#</span> <span class="title">#title#</span>',
            stepsOrientation: 1
        });
    });

    $(document).ready(function () {
        var form = $("#horizontal-wizard").show();
        form.steps({
            headerTag: "h3",
            bodyTag: "section",
            titleTemplate: '<span class="number">#index#</span> <span class="title">#title#</span>',
            stepsOrientation: 0
        });
    });

    $(document).ready(function () {
        var form = $("#horizontal-wizard-fullwidth").show();
        form.steps({
            headerTag: "h3",
            bodyTag: "section",
            titleTemplate: '<span class="number">#index#</span> <span class="title">#title#</span>',
            stepsOrientation: 0
        });
    });
});
