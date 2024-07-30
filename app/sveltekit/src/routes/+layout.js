import { csrf } from '$lib/session_data';

/** @type {import('./$types').LayoutLoad} */
export async function load(){

    if (typeof window !== 'undefined') {
        let csrfToken = window.localStorage.getItem('csrfToken');

        if (!csrfToken) {
            csrfToken = await csrf();
            window.localStorage.setItem('csrfToken', csrfToken)
        }
        console.log(csrfToken)
        return {
            csrfToken: csrfToken
        }
      }
    return {
        csrfToken: 'WRONG'
    }
}