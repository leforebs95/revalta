<script lang="ts">
    import { goto, afterNavigate } from '$app/navigation';
    import { callFlaskEndpoint } from '$lib/session_data';
    import { writable } from 'svelte/store';
    import RadioGroup from '$lib/RadioGroup.svelte';
    import SurveyQuestion from '$lib/SurveyQuestion.svelte';
    import TextArea from '$lib/TextArea.svelte';
    import NumberSelector from '$lib/NumberSelector.svelte';
    /** @type {import('./$types').PageData} */
    export let data;

    // let symptoms;
    const csrfToken = data.csrfToken;
    const symptoms = data.symptoms ?? [];
    console.log(symptoms);

    const addSymptom = async () => {
        try {
            const response = await fetch('/api/addSymptom', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    "X-CSRFToken": csrfToken
                },
                credentials: 'same-origin',
                body: JSON.stringify({
                    symptomName: $symptomNameValue,
                    symptomDescription: $symptomDescriptionValue,
                    numberSelector: $numberSelectorValue,
                    symptomTime: $symptomTimeValue,
                    symptomDuration: $symptomDurationValue
                }),
            });
        } catch (error) {
            console.error('Error:', error);
        }
    }

    let symptomNameValue = writable<string | null>(null);
    let symptomDescriptionValue = writable<string | null>(null);
    let numberSelectorValue = writable<number | null>(null);
    let symptomTimeValue = writable<string | null>(null);
    let symptomDurationValue = writable<number | null>(null);
    
    const timeOptions = ['Morning', 'Afternoon', 'Night'];
    const durationOptions = [1, 2, 3];

    function submitSymptomData() {
        addSymptom();
    }

    </script>
    
    <main class="flex overflow-hidden flex-col items-start px-4 pt-4 pb-20 bg-white">
      <header class="flex pt-4 left-[360px] top-[73px] bg-white min-h-[31px] w-full max-md:max-w-full"></header>
      <div class="Example w-[1119px] h-[830px] p-4 left-[360px] top-[73px] absolute bg-white flex-col justify-start items-start inline-flex">
            <section>
                <SurveyQuestion question="1. Did you experience any symptoms today?"/>
                <TextArea bind:value={symptomNameValue} />
            </section>
            
            <section>
                <SurveyQuestion question="2. Please describe the symptoms."/>
                <TextArea bind:value={symptomDescriptionValue} />
            </section>
            
            <section>
                <SurveyQuestion question="3. How many times did you experience this symptom today?"/>
                <NumberSelector bind:value={numberSelectorValue} />
            </section>
            
            <section>
                <SurveyQuestion question="4. When did this symptom occur?" subtext="Select one option." />
                <RadioGroup options={timeOptions} name="symptom-time" bind:value={symptomTimeValue} />
            </section>
            
            <section>
                <SurveyQuestion question="5. How long did each episode last?" subtext="Select one option." />
                <RadioGroup options={durationOptions} name="symptom-duration" bind:value={symptomDurationValue}/>
            </section>
            <section>
                <button on:submit={submitSymptomData} class="btn-submit">Submit</button>
            </section>
            <table>
                <thead>
                    <tr>
                        <th>Symptom Name</th>
                        <th>Symptom Description</th>
                        <th>Symptom Duration</th>
                    </tr>
                </thead>
                <tbody>
                    {#each symptoms as symptom}
                        <tr>
                            <td>{symptom.symptomName}</td>
                            <td>{symptom.symptomDescription}</td>
                            <td>{symptom.symptomDuration}</td>
                        </tr>
                    {/each}
                </tbody>
            </table>
        </div>
    </main>