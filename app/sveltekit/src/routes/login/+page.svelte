<script lang="ts">
    import LoginCard from "$lib/components/LoginCard.svelte";
	import { onMount } from "svelte";
    /** @type {import('./$types').PageData} */
	export let data;
    
	let csrfToken: string | null = data.token;
    console.log("Login Page token: " + csrfToken)
</script>

<header class="absolute">
    <div class="mt-10 mb-10 ml-10 col-span-1 text-whisper font-sans font-bold text-4xl">
        Nivalta
    </div>
</header>


<main class="flex justify-center items-center mx-auto gap-52 border border-black h-screen">
    <div class="flex items-center align-middle justify-center h-auto flex-wrap w-[500px] ">
        <img src="/images/hero.svg" alt="logo" class="mb-20">
        <p class="text-white font-sans text-2xl text-wrap text-center">Discover the power of personalized health insights and seamless tracking with Nivalta.</p>
    </div>
    <div class="rounded-lg">
        <LoginCard bind:csrfToken/>
    </div>

</main>