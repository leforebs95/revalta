import { getCsrf, validatecsrf } from '$lib/session_data';

/** @type {import('./$types').PageLoad} */
export async function load(){

    if (typeof window !== 'undefined') {
        let csrfToken = window.sessionStorage.getItem('csrfToken');

        const validation =  await validatecsrf(csrfToken);
        if (!validation) {
            csrfToken = await getCsrf();
            window.sessionStorage.setItem('csrfToken', csrfToken)
        }
        
        return {
            csrfToken: csrfToken
        }
      }
}