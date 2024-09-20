<script>
	import { isOverlayOpen } from './../stores/Overlay.js';
	import '../app.css';
	import Overlay from '$lib/components/Overlay.svelte';
</script>

<header>
	{#if $isOverlayOpen}
		<Overlay>
			<div class="bg-whisper sm:rounded-lg">
				<div class="px-4 py-5 sm:p-6">
					<h3 class="text-base font-semibold leading-6 text-gray-900">
						Provide the email associated with your account
					</h3>
					<form class="mt-5 sm:flex sm:items-center z-0">
						<div class="w-full sm:max-w-xs">
							<label for="email" class="sr-only">Email</label>
							<input
								type="email"
								name="email"
								id="email"
								class="block w-full rounded-md border-0 py-1.5 px-1 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
								placeholder="email@example.com"
								required
							/>
						</div>
						<button
							type="submit"
							class="mt-3 inline-flex w-full items-center justify-center rounded-md bg-nivaltaBlue px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 sm:ml-3 sm:mt-0 sm:w-auto"
							>Submit</button
						>
					</form>
				</div>
			</div>
		</Overlay>
	{/if}
</header>

<slot />

