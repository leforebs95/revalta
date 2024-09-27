import { getSession } from "$lib/session_data";

// export const ssr = false;

// /** @type {import('./$types').LayoutLoad} */
// export async function load() {
//     const sessionData = await getSession();
//   return {
//     sessionData,
//   };
// }

/** @type {import('./$types').LayoutLoad} */
export async function load({ url, fetch }) {
  let sessionData = {};
  let request_url = url.origin + "/api/getsession";
  try {
    const sessionRes = await fetch(request_url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "same-origin",
    });
    sessionData = await sessionRes.json();
  } catch (error) {
    console.error("Failed to fetch session data:", error);
  }
  console.log("sessionData at load: ", sessionData);  
  return {
    sessionData,
  };
}