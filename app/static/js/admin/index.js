var Admin = {
    forms:  [{id: 'form_domain_inactive', url:'/admin/domain_inactive/'}],

    set_events: () => {
        Admin.selected_action('inactive_all', '/admin/inactive/');
        Admin.selected_action('active_all', '/admin/active/');
        Admin.selected_action('delete_all', '/admin/delete/');
        
        fetch_forms(Admin.forms)
    },

    selected_action: (action, url) => {
        document.getElementById(action).addEventListener('click', () => {
            let ids = Array.from(document.getElementsByClassName('row_url')).filter(e => e.firstElementChild.firstElementChild.firstElementChild.checked).map(e => e.id);

            fetch(url, {
                method: "POST",
                headers: {
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                   ids : ids
                }),
            })
            .then(res => {
                if (res.status != 200) {
                    console.warn(res);
                    $.SOW.core.toast.show('danger', 'Ошибка', 'Что-то пошло не так...', 'top-right', 3000, true)
                    return;
                }

                if (res.redirected) {
                    window.location.href = res.url
                    return;
                }

                return res.json()
            }, err => console.error(err))
            .then(json => {
                if (json.status == "fail")
                    $.SOW.core.toast.show('danger', 'Ошибка', json.text, 'top-right', 3000, true)
                else {
                    button.parentElement.parentElement.parentElement.remove();
                    $.SOW.core.toast.show('success', 'Успех', json.text, 'top-right', 3000, true)
                }
            })
            .catch(warn => console.warn(warn))
        })
    }
}

Admin.set_events();