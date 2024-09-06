import { getCsrf, validatecsrf } from '$lib/session_data';

/** @type {import('./$types').PageLoad} */
export async function load(){

    if (typeof window !== 'undefined') {
        let csrfToken = window.sessionStorage.getItem('csrfToken');

        const validation =  await validatecsrf(csrfToken);
        console.log("Current csrf token status: " + validation)
        if (!validation) {
            csrfToken = await getCsrf();
            console.log("New csrf token: " + csrfToken)
            window.sessionStorage.setItem('csrfToken', csrfToken)
        }
        
        console.log("Current CSRF Token is: " + csrfToken)
        return {
            csrfToken: csrfToken
        }
      }
}