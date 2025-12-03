const SIGNIN_FORM = document.querySelector('section#signin-section > form');
const SIGNUP_FORM = document.querySelector('section#signup-section > form');

SIGNIN_FORM.onsubmit = (event) => {
    event.preventDefault();

    const MESSAGE_SECTION = SIGNIN_FORM.parentNode.querySelector('section.messages-section');
    const formData = new FormData(SIGNIN_FORM);
    const headers = new Headers();

    const request = new Request(SIGNIN_FORM.action, {
        method: 'POST',
        headers: headers,
        body: formData,
    })

    fetch(request).then( (response) => {        
        if (!response.ok) {
            response.text().then( (data) => {
                const jsondata = JSON.parse(data);
                displayMessage(MESSAGE_SECTION, jsondata.message, jsondata.type);
            });
        }
        else if (response.redirected) {
            window.location.href = response.url;
        }
    });
};

SIGNUP_FORM.onsubmit = (event) => {
    event.preventDefault();

    const MESSAGE_SECTION = SIGNUP_FORM.parentNode.querySelector('section.messages-section');
    const formData = new FormData(SIGNUP_FORM);
    const headers = new Headers();
    const request = new Request(SIGNUP_FORM.action, {
        method: 'POST',
        headers: headers,
        body: formData,
    })

    fetch(request).then( (response) => {
        if (!response.ok) {
            response.text().then( (data) => {
                const jsondata = JSON.parse(data);
                displayMessage(MESSAGE_SECTION, jsondata.message, jsondata.type);
            });
        }
        else if (response.redirected) {
            window.location.href = response.url;
        };
    });
};