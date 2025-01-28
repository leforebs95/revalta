<script lang="ts">
    export interface SurveyQuestionProps {
        question: string;
        subtext: string;
    }
    
    export let question: string;
    export let subtext: string = '';
    </script>
    
    <div class="overflow-hidden self-stretch pt-4 pr-2 pb-2 w-full text-base font-bold text-black bg-white max-md:max-w-full">
        {question}
        {#if subtext}
            <span class="italic text-stone-500">{subtext}</span>
        {/if}
    </div>