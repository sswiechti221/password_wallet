function section_change_to(section_id, section_namespace) {
    const sections = document.querySelectorAll(`.${section_namespace}`);
    sections.forEach((section) => {
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
