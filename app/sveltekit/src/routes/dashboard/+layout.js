import { callFlaskEndpoint } from '$lib/session_data';

/** @type {import('./$types').LayoutLoad} */
export async function load({ fetch }) {
    let symptoms;
    let sessionData = await callFlaskEndpoint(fetch, '/api/getsession', 'GET');
    if (sessionData.response_data.login) {
        symptoms = (await callFlaskEndpoint(fetch, '/api/symptoms', 'GET')).response_data;
    }
    return {
        "sessionData": sessionData.response_data,
        "symptoms": symptoms
    }
}