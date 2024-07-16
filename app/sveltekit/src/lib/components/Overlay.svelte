<script>
	import { isOverlayOpen } from '../../stores/Overlay';
</script>

<div
	class="w-screen h-screen fixed top-0 left-0 flex justify-center items-center bg-slate-800 opacity-90 z-10"
>
	<div
		class="text-nivaltaBlue bg-whisper rounded-md px-8 py-10 relative max-w-lg shadow-xl shadow-slate-700 z-20"
	>
		<button
			class="absolute top-2 right-3 text-4xl text-gray-500 hover:-translate-y-0.5 transition-transform"
			on:click={() => {
				isOverlayOpen.set(false);
			}}>&times;</button
		>
		<slot />
	</div>
</div>
