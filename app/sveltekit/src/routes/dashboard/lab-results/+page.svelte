<script lang="ts">
    import { enhance } from '$app/forms';
	import { callFlaskEndpoint } from '$lib/session_data';

    import type { ActionData } from './$types';
    export let form: ActionData;
    console.log(`form: `, form);

    import type { PageData } from './$types';
    export let data: PageData;
    console.log(`data: `, data);

    $: if (form?.success) {
        console.log(`form.flaskParams: `, form.flaskParams);
        callFlaskEndpoint(fetch, '/api/addResult', 'POST', {'X-CSRFToken': data.sessionData.csrfToken}, form.flaskParams);
    }

</script>

<main class="flex overflow-hidden flex-col items-start px-4 pt-4 pb-20 bg-white">
    <header class="flex pt-4 left-[360px] top-[73px] bg-white min-h-[31px] w-full max-md:max-w-full"></header>
    <div class="Example w-[1119px] h-[830px] p-4 left-[360px] top-[73px] absolute bg-white flex-col justify-start items-start inline-flex">
    <form method="post" enctype="multipart/form-data" use:enhance>
        <label for="fileDescription">File Description:</label>
        <input type="text" id="fileDescription" name="fileDescription" />
        <input type="file" name="file" />
        <button>Upload</button>
    </form>
    </div>
</main>