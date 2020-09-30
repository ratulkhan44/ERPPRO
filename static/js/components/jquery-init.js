       $(function() {
            $("#commentForm").validate({})
        });

        jQuery.validator.setDefaults({
            debug: true,
            success: "valid"
        });
        $("#myform").validate({
            rules: {
                firstname: {
                    required: true,
                    minlength: 2
                },
                lastname: {
                    required: true,
                    minlength: 2
                },
                username: {
                    required: true,
                    range: [2, 23]
                },
                password: {
                    required: true
                },
                confirmpasswords: {
                    equalTo: "#password",
                    required: true
                },
                email: {
                    required: true,
                    email: true
                },
                date: {
                    required: true,
                    date: true
                },
                url: {
                    required: true,
                    url: true
                },
                city: {
                    required: true,
                    minlength: 2
                },
                state: {
                    required: true,
                    minlength: 2
                },
                zip: {
                    required: true,
                    minlength: 2
                },
                image: {
                    required: true,
                    accept: "image/*"
                }
            }
        });