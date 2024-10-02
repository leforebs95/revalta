<div class="flex overflow-hidden flex-wrap gap-2 justify-center items-start py-2 text-base font-bold text-center text-black whitespace-nowrap bg-white max-md:max-w-full">
  {#each Array(5) as _, i}
    <button 
      class="overflow-hidden flex-1 shrink gap-2.5 self-stretch p-2.5 bg-white rounded-lg border border-solid border-stone-500 shadow-[0px_2px_1px_rgba(0,0,0,0.1)] w-[106px]"
    >
      {i === 4 ? '5+' : i + 1}
    </button>
  {/each}
</div>