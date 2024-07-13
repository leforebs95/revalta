import { c as create_ssr_component, a as subscribe, v as validate_component } from './ssr-B8ma60Mg.js';
import { w as writable } from './index-DMw_fPIZ.js';

const isOverlayOpen = writable(false);
const Overlay = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  return `<div class="w-screen h-screen fixed top-0 left-0 flex justify-center items-center bg-slate-800 opacity-90 z-10"><div class="text-nivaltaBlue bg-whisper rounded-md px-8 py-10 relative max-w-lg shadow-xl shadow-slate-700 z-20"><button class="absolute top-2 right-3 text-4xl text-gray-500 hover:-translate-y-0.5 transition-transform" data-svelte-h="svelte-rwq8cf">×</button> ${slots.default ? slots.default({}) : ``}</div></div>`;
});
const Layout = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let $isOverlayOpen, $$unsubscribe_isOverlayOpen;
  $$unsubscribe_isOverlayOpen = subscribe(isOverlayOpen, (value) => $isOverlayOpen = value);
  $$unsubscribe_isOverlayOpen();
  return `<header>${$isOverlayOpen ? `${validate_component(Overlay, "Overlay").$$render($$result, {}, {}, {
    default: () => {
      return `<div class="bg-whisper sm:rounded-lg" data-svelte-h="svelte-10lhhy2"><div class="px-4 py-5 sm:p-6"><h3 class="text-base font-semibold leading-6 text-gray-900">Provide the email associated with your account</h3> <form class="mt-5 sm:flex sm:items-center z-0"><div class="w-full sm:max-w-xs"><label for="email" class="sr-only">Email</label> <input type="email" name="email" id="email" class="block w-full rounded-md border-0 py-1.5 px-1 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6" placeholder="email@example.com" required></div> <button type="submit" class="mt-3 inline-flex w-full items-center justify-center rounded-md bg-nivaltaBlue px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 sm:ml-3 sm:mt-0 sm:w-auto">Submit</button></form></div></div>`;
    }
  })}` : ``}</header> <div class="grid min-h-screen grid-cols-12 bg-nivaltaBlue"><main class="col-span-12">${slots.default ? slots.default({}) : ``}</main></div>`;
});

export { Layout as default };
//# sourceMappingURL=_layout.svelte-YblmFH0N.js.map
