import { callFlaskEndpoint } from '$lib/session_data';

/** @type {import('./$types').PageLoad} */
export async function load({ fetch }) {
    const sessionData = await callFlaskEndpoint(fetch, "/api/getsession", "GET");
    const csrfToken = await callFlaskEndpoint(fetch, "/api/getcsrf", "GET");
    return {
        sessionData: sessionData?.response_data,
        csrfToken: csrfToken?.response_headers.get("X-CSRFToken"),
    }
}