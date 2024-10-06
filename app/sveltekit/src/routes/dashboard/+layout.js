import { callFlaskEndpoint } from '$lib/session_data';

/** @type {import('./$types').LayoutLoad} */
export async function load({ fetch }) {
    const csrfToken = await callFlaskEndpoint(fetch, "/api/getcsrf", "GET");
    let sessionData = {csrfToken: csrfToken?.response_headers.get("X-CSRFToken")}
    let symptoms;
    let sessionRes = await callFlaskEndpoint(fetch, '/api/getsession', 'GET');
    sessionData = { ...sessionData, ...sessionRes.response_data };
    if (sessionData.login) {
        symptoms = (await callFlaskEndpoint(fetch, '/api/symptoms', 'GET')).response_data;
    }
    return {
        "sessionData": sessionData,
        "symptoms": symptoms
    }
}