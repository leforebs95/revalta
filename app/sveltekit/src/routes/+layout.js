import { csrf } from '$lib/session_data';

/** @type {import('./$types').LayoutLoad} */
export function load() {

    return csrf().then(token => {
        console.log("CSRFToken Creation: " + token);
        return {
            token: token
        };
    });
}