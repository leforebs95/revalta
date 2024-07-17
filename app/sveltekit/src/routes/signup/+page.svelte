<script lang="ts">
	import { onMount } from 'svelte';
	import { enhance } from '$app/forms';
	import { goto } from '$app/navigation';
	import { csrf, getSession, login } from '../../session_data';

	let firstName: string;
	let lastName: string;
	let email: string;
	let password: string;
	let confirmPassword: string;
	let csrfToken: string | null;
	let isAuthenticated: boolean = false;

	onMount(() => {
		getSession().then(authentication =>{
			isAuthenticated = authentication;
		});
		console.log(isAuthenticated)
		if (!isAuthenticated) {
			csrf().then(token => {
				csrfToken = token;
			});
		}
	});
	
	const signup = () => {
		fetch("./api/signup")
		.then((res) => {
			res.json()
			console.log(res.json())
		})
	}

</script>

<div class="flex h-screen w-screen justify-center items-center">
	<div class="flex bg-whisper h-[600px] w-[400px] rounded-xl items-center justify-center">
		<form>
			<div class="flex items-center">
				<h1 class="text-nivaltaBlue font-bold text-xl">Sign Up</h1>
			</div>
			<div class="space-y-12">
				<div class="border-b border-gray-900/10 pb-12">
					<div class="mt-10 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
						<div class="sm:col-span-3">
							<label for="first-name" class="block text-sm font-medium leading-6 text-gray-900"
								>First name</label
							>
							<div class="mt-2">
								<input
									type="text"
									name="first-name"
									id="first-name"
									autocomplete="given-name"
									bind:value={firstName}
									class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
								/>
							</div>
						</div>

						<div class="sm:col-span-3">
							<label for="last-name" class="block text-sm font-medium leading-6 text-gray-900"
								>Last name</label
							>
							<div class="mt-2">
								<input
									type="text"
									name="last-name"
									id="last-name"
									autocomplete="family-name"
									bind:value={lastName}
									class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
								/>
							</div>
						</div>

						<div class="sm:col-span-4 lg:col-span-6">
							<label for="email" class="block text-sm font-medium leading-6 text-gray-900"
								>Email address</label
							>
							<div class="mt-2">
								<input
									id="email"
									name="email"
									type="email"
									autocomplete="email"
									bind:value={email}
									class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
								/>
							</div>
						</div>

						<div class="sm:col-span-4 lg:col-span-6">
							<label for="email" class="block text-sm font-medium leading-6 text-gray-900"
								>Password</label
							>
							<div class="mt-2">
								<input
									id="password"
									name="password"
									type="password"
									bind:value={password}
									class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
								/>
							</div>
						</div>

						<div class="sm:col-span-4 lg:col-span-6">
							<label for="email" class="block text-sm font-medium leading-6 text-gray-900"
								>Confirm Password</label
							>
							<div class="mt-2">
								<input
									id="password"
									name="password"
									type="password"
									bind:value={confirmPassword}
									class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
								/>
							</div>
						</div>
					</div>
				</div>
			</div>

			<div class="mt-6 flex items-center justify-end gap-x-6">
				<button
					type="button"
					class="text-sm font-semibold leading-6 text-gray-900"
					on:click={() => goto('/')}>Cancel</button
				>
				<button
					type="button"
					class="rounded-md bg-nivaltaBlue px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
					on:click={signup}
					>Save</button
				>
			</div>
		</form>
	</div>
</div>
