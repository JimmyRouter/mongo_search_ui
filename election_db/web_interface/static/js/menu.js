function toggleSubmenu(mainGroup) {
    let submenu = document.getElementById(mainGroup + 'Menu');
    if (submenu.style.display === 'block') {
        submenu.style.display = 'none';
    } else {
        submenu.style.display = 'block';
    }
}

function expandDiv(famHead) {
    let fambox = document.getElementById('fam_box' + famHead);
    if (fambox.classList.contains('expanded')) {
        fambox.classList.remove('expanded');
    } else {
        fambox.classList.add('expanded');
    }
}


let edit_btns = document.querySelectorAll(".btn-edit");
edit_btns.forEach(function(edit_btn) {
    edit_btn.addEventListener("click", function(ev) {
        ev.stopPropagation();

    });
});

function toggleEditable(memberID) {
    let field_set = document.getElementById(memberID);
    if (field_set.disabled === true) {
        field_set.disabled = false;
    } else {
        field_set.disabled = true;
    }
}
