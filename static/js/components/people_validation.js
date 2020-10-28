const nameField = document.querySelector("#name");
const nameFeedback = document.querySelector(".invalid-name-feedback")

nameField.addEventListener('keyup', (e) =>{
    console.log("xyz")

    const nameValue = e.target.value;
    console.log(nameValue);

    nameField.classList.remove("is-invalid");
    nameFeedback.style.display="none";

    if(nameValue.length > 0) {
        fetch("/people/validate-username/", {
            body: JSON.stringify({name:nameValue}),
            method:'POST',
        })
        .then((res)=> res.json())
        .then((data) =>{
            console.log(data);
            if(data.name_error){
                nameField.classList.add("is-invalid");
                nameFeedback.style.display="block";
                nameFeedback.innerHTML=`<p>${data.name_error}</p>`
            }
        });
    }     
    
})


//for contact no validation

const contactField = document.querySelector("#contact");
const contactFeedback = document.querySelector(".invalid-contact-feedback")

contactField.addEventListener('keyup', (e) =>{
    console.log("xyz")

    const contactValue = e.target.value;
    console.log(contactValue);

    contactField.classList.remove("is-invalid");
    contactFeedback.style.display="none";

    if(contactValue.length > 0) {
        fetch("/people/validate-contact/", {
            body: JSON.stringify({contact:contactValue}),
            method:'POST',
        })
        .then((res)=> res.json())
        .then((data) =>{
            console.log(data);
            if(data.contact_error){
                contactField.classList.add("is-invalid");
                contactFeedback.style.display="block";
                contactFeedback.innerHTML=`<p>${data.contact_error}</p>`
            }
        });
    }     
    
})


// Nid Validation

const nidField = document.querySelector("#nid");
const nidFeedback = document.querySelector(".invalid-nid-feedback")

nidField.addEventListener('keyup', (e) =>{
    console.log("xyz")

    const nidValue = e.target.value;
    console.log(nidValue);

    nidField.classList.remove("is-invalid");
    nidFeedback.style.display="none";

    if(nidValue.length > 0) {
        fetch("/people/validate-nid/", {
            body: JSON.stringify({nid:nidValue}),
            method:'POST',
        })
        .then((res)=> res.json())
        .then((data) =>{
            console.log(data);
            if(data.nid_error){
                nidField.classList.add("is-invalid");
                nidFeedback.style.display="block";
                nidFeedback.innerHTML=`<p>${data.nid_error}</p>`
            }
        });
    }     
    
})

// Passport no validation

const passportField = document.querySelector("#passport");
const passportFeedback = document.querySelector(".invalid-passport-feedback")

passportField.addEventListener('keyup', (e) =>{
    console.log("xyz")

    const passportValue = e.target.value;
    console.log(passportValue);

    passportField.classList.remove("is-invalid");
    passportFeedback.style.display="none";

    if(passportValue.length > 0) {
        fetch("/people/validate-passport/", {
            body: JSON.stringify({passport:passportValue}),
            method:'POST',
        })
        .then((res)=> res.json())
        .then((data) =>{
            console.log(data);
            if(data.passport_error){
                passportField.classList.add("is-invalid");
                passportFeedback.style.display="block";
                passportFeedback.innerHTML=`<p>${data.passport_error}</p>`
            }
        });
    }     
    
})

//Tracking validation
const trackingField = document.querySelector("#tracking");
const trackingFeedback = document.querySelector(".invalid-tracking-feedback")

trackingField.addEventListener('keyup', (e) =>{
    console.log("xyz")

    const trackingValue = e.target.value;
    console.log(trackingValue);

    trackingField.classList.remove("is-invalid");
    trackingFeedback.style.display="none";

    if(trackingValue.length > 0) {
        fetch("/people/tracking-passport/", {
            body: JSON.stringify({tracking:trackingValue}),
            method:'POST',
        })
        .then((res)=> res.json())
        .then((data) =>{
            console.log(data);
            if(data.tracking_error){
                trackingField.classList.add("is-invalid");
                trackingFeedback.style.display="block";
                trackingFeedback.innerHTML=`<p>${data.tracking_error}</p>`
            }
        });
    }     
    
})

// Email validation

const emailField = document.querySelector("#email");
const emailFeedback = document.querySelector(".invalid-email-feedback")

emailField.addEventListener('keyup', (e) =>{
    console.log("xyz")

    const emailValue = e.target.value;
    console.log(emailValue);

    emailField.classList.remove("is-invalid");
    emailFeedback.style.display="none";

    if(emailValue.length > 0) {
        fetch("/people/validate-email/", {
            body: JSON.stringify({email:emailValue}),
            method:'POST',
        })
        .then((res)=> res.json())
        .then((data) =>{
            console.log(data);
            if(data.email_error){
                emailField.classList.add("is-invalid");
                emailFeedback.style.display="block";
                emailFeedback.innerHTML=`<p>${data.email_error}</p>`
            }
        });
    }     
    
})