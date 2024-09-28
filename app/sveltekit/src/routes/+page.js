import { callFlaskEndpoint } from "$lib/session_data";


/** @type {import('./$types').PageLoad} */
export async function load({ fetch }) {
  const sessionData = await callFlaskEndpoint(fetch, "/api/getsession", "GET");
  return {
    "sessionData": sessionData.response_data,
  };
}