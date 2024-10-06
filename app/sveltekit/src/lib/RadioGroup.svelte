<script lang="ts">
    import { writable, type Writable } from 'svelte/store';
    
    export interface RadioGroupProps {
        options: string[];
        name: string;
    }
    
    export let options: string[];
    export let name: string;
    export let value: Writable<string | null> = writable(null);
</script>
    
    <fieldset>
        {#each options as option}
            <div class="flex overflow-hidden flex-wrap items-start pt-2 pr-2 max-w-full bg-white w-[563px]">
                <div class="flex flex-col grow shrink items-start pr-2 pb-0.5 bg-white w-[22px]">
                    <input
                        type="radio"
                        id={`${name}-${option}`}
                        {name}
                        value={option}
                        class="w-5 h-5 bg-white rounded-full border border-black border-solid min-h-[20px] shadow-[0px_1px_2px_rgba(0,0,0,0.25)]"
                        bind:group={$value}
                    />
                </div>
                <label for={`${name}-${option}`} class="grow shrink text-base text-black min-w-[240px] w-[521px] max-md:max-w-full">
                    {option}
                </label>
            </div>
        {/each}
    </fieldset>