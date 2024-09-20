<script lang="ts">
    import { writable, type Writable } from 'svelte/store';
    
    export let value: Writable<string> = writable('');
    </script>
    
    <div class="flex overflow-hidden flex-col justify-center self-stretch py-2 w-full bg-white min-h-[127px] max-md:max-w-full">
        <textarea
            class="flex flex-1 w-full bg-white rounded-lg border border-solid border-stone-500 min-h-[111px] shadow-[0px_2px_1px_rgba(0,0,0,0.1)] max-md:max-w-full p-2"
            aria-label="Symptom description"
            bind:value={$value}
        ></textarea>
    </div>