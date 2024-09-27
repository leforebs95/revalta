/** @type {import('@sveltejs/kit').HandleFetch} */
export async function handleFetch({ request, fetch }) {
	console.log("request.url: ", request.url);
    if (request.url.startsWith('http://localhost/')) {
		// clone the original request, but change the URL
        request = new Request(
			request.url.replace('http://localhost/', 'http://flask-server:5000/'),
			request
		);
        console.log("request.url after replace: ", request.url);
	}

	return fetch(request);
}