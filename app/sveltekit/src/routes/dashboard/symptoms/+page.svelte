<script lang="ts">
    import { writable } from 'svelte/store';
    import RadioGroup from './RadioGroup.svelte';
    import SurveyQuestion from './SurveyQuestion.svelte';
    import TextArea from './TextArea.svelte';
    import {
      NumberSelector,
    } from './SurveyLib';
    
    // let textAreaValue1;
    // let textAreaValue2;
    // const numberSelectorValue = writable<number | null>(null);
    // let radioGroupValue1;
    // let radioGroupValue2;
    
    const timeOptions = ['Morning', 'Afternoon', 'Night'];
    const durationOptions = ['Less than 5 minutes', '5-15 minutes', '15-30 minutes'];
    </script>
    
    <main class="flex overflow-hidden flex-col items-start px-4 pt-4 pb-20 bg-white">
      <header class="flex pt-4 left-[360px] top-[73px] bg-white min-h-[31px] w-full max-md:max-w-full"></header>
      <div class="Example w-[1119px] h-[830px] p-4 left-[360px] top-[73px] absolute bg-white flex-col justify-start items-start inline-flex">
            <section>
                <SurveyQuestion question="1. Did you experience any symptoms today?"/>
                <TextArea bind:value={textAreaValue1} />
            </section>
            
            <section>
                <SurveyQuestion question="Please describe the symptoms."/>
                <TextArea bind:value={textAreaValue2} />
            </section>
            
            <section>
                <SurveyQuestion question="3. How many times did you experience this symptom today?"/>
                <!-- {@html NumberSelector()} -->
            </section>
            
            <section>
                <SurveyQuestion question="4. When did this symptom occur?" subtext="Select one option." />
                <RadioGroup options={timeOptions} name="symptom-time" bind:value={radioGroupValue1} />
            </section>
            
            <section>
                <SurveyQuestion question="5. How long did each episode last?" subtext="Select one option." />
                <RadioGroup options={durationOptions} name="symptom-duration" bind:value={radioGroupValue2}/>
            </section>
        </div>
    </main>