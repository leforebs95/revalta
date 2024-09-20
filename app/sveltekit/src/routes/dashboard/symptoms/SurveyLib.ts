import { writable } from 'svelte/store';

export interface SurveyQuestion {
  question: string;
  subtext?: string;
}

export const createTextArea = () => {
  const { subscribe, set } = writable('');
  return {
    subscribe,
    set,
    reset: () => set('')
  };
};

export const createNumberSelector = () => {
  const { subscribe, set } = writable<number | null>(null);
  return {
    subscribe,
    set,
    reset: () => set(null)
  };
};

export const createRadioGroup = () => {
  const { subscribe, set } = writable<string | null>(null);
  return {
    subscribe,
    set,
    reset: () => set(null)
  };
};

export const SurveyQuestion = ({ question, subtext = '' }: SurveyQuestion) => `
  <div class="overflow-hidden self-stretch pt-4 pr-2 pb-2 w-full text-base font-bold text-black bg-white max-md:max-w-full">
    ${question}
    ${subtext ? `<span class="italic text-stone-500">${subtext}</span>` : ''}
  </div>
`;

export const TextArea = () => `
  <div class="flex overflow-hidden flex-col justify-center self-stretch py-2 w-full bg-white min-h-[127px] max-md:max-w-full">
    <textarea
      class="flex flex-1 w-full bg-white rounded-lg border border-solid border-stone-500 min-h-[111px] shadow-[0px_2px_1px_rgba(0,0,0,0.1)] max-md:max-w-full p-2"
      aria-label="Symptom description"
      bind:value={$textAreaValue}
    ></textarea>
  </div>
`;

export const NumberSelector = () => `
    <div class="flex overflow-hidden flex-wrap gap-2 justify-center items-start py-2 text-base font-bold text-center text-black whitespace-nowrap bg-white max-md:max-w-full">
        ${Array.from({ length: 5 }, (_, i) => `
            <button
                class="overflow-hidden flex-1 shrink gap-2.5 self-stretch p-2.5 bg-white rounded-lg border border-solid border-stone-500 shadow-[0px_2px_1px_rgba(0,0,0,0.1)] w-[106px]"
                on:click={}>
                ${i}
            </button>
        `).join('')}
    </div>
`;

export const RadioGroup = ({ options, name }: { options: string[], name: string }) => `
  <fieldset>
    {#each options as option}
      <div class="flex overflow-hidden flex-wrap items-start pt-2 pr-2 max-w-full bg-white w-[563px]">
        <div class="flex flex-col grow shrink items-start pr-2 pb-0.5 bg-white w-[22px]">
          <input
            type="radio"
            id={\`${name}-\${option}\`}
            {name}
            value={option}
            class="w-5 h-5 bg-white rounded-full border border-black border-solid min-h-[20px] shadow-[0px_1px_2px_rgba(0,0,0,0.25)]"
            bind:group={$radioGroupValue}
          />
        </div>
        <label for={\`${name}-\${option}\`} class="grow shrink text-base text-black min-w-[240px] w-[521px] max-md:max-w-full">
          {option}
        </label>
      </div>
    {/each}
  </fieldset>
`;