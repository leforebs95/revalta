import { callFlaskEndpoint } from "$lib/session_data";

export const ssr = false;

/** @type {import('./$types').PageLoad} */
export async function load({ fetch }) {
    const csrfToken = await callFlaskEndpoint(fetch, "/api/getcsrf", "GET");
    return {
        csrfToken: csrfToken?.response_headers.get("X-CSRFToken"),
    }
    
}