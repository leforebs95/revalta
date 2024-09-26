import { getSession } from "$lib/session_data";

/** @type {import('./$types').LayoutLoad} */
export async function load() {
    const sessionData = await getSession();
  return {
    sessionData,
  };
}