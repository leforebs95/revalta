import { callFlaskEndpoint } from '$lib/session_data';

export async function load({ fetch }) {
    let sessionData = await callFlaskEndpoint(fetch, '/api/getsession', 'GET');
    return {
        "sessionData": sessionData.response_data
    }
}