const SAVE_PASSWORD_SECTION = document.querySelector('section#save-password-section');
const ENCRYPTION_INFO_URL = "/encryption/info/"

function update_encryption_info(encryption_name, encryption_info_section) {
    fetch(ENCRYPTION_INFO_URL + encryption_name)
    .then( (response) => response.json())
    .then( (info_data) => {
        encryption_info_section.querySelectorAll("dd[field]").forEach( ((dd) => {
            dd.innerText = info_data[dd.getAttribute("field")];
        }));
        SAVE_PASSWORD_SECTION.querySelector('input[name="encryption-key"]').attributes['pattern'].value = info_data["key-regex"];
    });
};

if (SAVE_PASSWORD_SECTION) {
    const SAVE_PASSWORD_FORM = SAVE_PASSWORD_SECTION.querySelector('form');
    const ENCRYPTION_METHOD_SELECT = SAVE_PASSWORD_FORM.querySelector('select[name="encryption-method"]');
    
    const ENCRYPTION_INFO_SECTION = SAVE_PASSWORD_SECTION.querySelector('section#encryption-info-section');

    ENCRYPTION_METHOD_SELECT.onchange = (event) => {
        update_encryption_info(event.target.value, ENCRYPTION_INFO_SECTION);   
    };
    update_encryption_info(ENCRYPTION_METHOD_SELECT.value, ENCRYPTION_INFO_SECTION);
};