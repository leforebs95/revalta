
export async function callFlaskEndpoint(
    fetch: (input: RequestInfo, init?: RequestInit) => Promise<Response>,
    endpoint: string,
    method: 'POST' | 'GET' | 'DELETE' | 'PUT' | 'PATCH',
    headers: Record<string, string> = {},
    body: Record<string, any> = {}
) {
    const defaultHeaders = {
        "Content-Type": "application/json",
    };
    const combinedHeaders = { ...defaultHeaders, ...headers };
    console.log(`HTTP ${method} to ${endpoint}`, { combinedHeaders, body });
    try {
        const res = await fetch(endpoint, {
            method: method,
            credentials: "same-origin",
            headers: combinedHeaders,
            body: method !== 'GET' ? JSON.stringify(body) : undefined,
        });
        const data = await res.json();
        return {
            response_headers: res.headers,
            response_data: data,
        };
    } catch (error) {
        console.error(`Failed to call endpoint: ${endpoint}`, { error });
        throw error;
    }
}
