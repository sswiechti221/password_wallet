function displayMessage(where, message, type) {
    const p = document.createElement('p');
    p.classList.add(type + '-p');
    p.textContent = message;
    where.innerHTML = p.outerHTML; 
};

function section_change_to(section_id) {
    const sections = document.querySelectorAll("main > section");
    if (sections.length == 0) return;

    sections.forEach( (section) => {
        if (section.id == section_id) {
            section.classList.remove("disabled");
            section.classList.add("active");
        }
        else {
            section.classList.remove("active");
            section.classList.add("disabled");
        };
    });
};

const CONTROL_SECTION = document.querySelector("nav");
for (let button of CONTROL_SECTION.getElementsByTagName("button")) {
        button.onclick = section_change_to.bind(null, button.id.replace("-button", "-section"));   
    };

