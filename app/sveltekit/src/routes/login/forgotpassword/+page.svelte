<script lang="ts">
	import { goto } from '$app/navigation';
</script>

<div class="flex h-screen w-screen justify-center items-center">
	<div class="flex bg-whisper h-[250px] w-[350px] rounded-xl items-center justify-center">
		<form>
			<h1 class="text-nivaltaBlue font-bold text-xl flex justify-center">Forgot Password</h1>
			<div class="space-y-12 w-[300px]">
				<div class="border-b border-gray-900/10 pb-12">
					<div class="mt-5 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6 w-full">
						<div class="sm:col-span-4 lg:col-span-9">
							<label for="email" class="block text-sm font-medium leading-6 text-gray-900"
								>Email address</label
							>
							<div class="mt-2">
								<input
									id="email"
									name="email"
									type="email"
									autocomplete="email"
									placeholder="Enter email associated with your account."
									class="block w-full rounded-md border-0 py-1.5 px-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
								/>
							</div>
						</div>
					</div>
				</div>
			</div>
			<div class="mt-2 flex items-center justify-end gap-x-6">
				<button
					type="button"
					class="text-sm font-semibold leading-6 text-gray-900"
					on:click={() => goto('/')}>Cancel</button
				>
				<button
					type="submit"
					class="rounded-md bg-nivaltaBlue px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
					>Save</button
				>
			</div>
		</form>
	</div>
</div>
