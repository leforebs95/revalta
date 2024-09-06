import { csrf } from '$lib/session_data';

/** @type {import('./$types').PageLoad} */
export async function load(){

    if (typeof window !== 'undefined') {
        let csrfToken = window.sessionStorage.getItem('csrfToken');

        if (!csrfToken) {
            console.log("Retrieving new CSRF Token")
            csrfToken = await csrf();
            window.sessionStorage.setItem('csrfToken', csrfToken)
        }
        console.log("Current CSRF Token is: " + csrfToken)
        return {
            csrfToken: csrfToken
        }
      }
}