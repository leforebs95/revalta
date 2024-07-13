

export const index = 3;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/_user_/_page.svelte.js')).default;
export const imports = ["_app/immutable/nodes/3.C6eQXBWe.js","_app/immutable/chunks/scheduler.Bmg8oFKD.js","_app/immutable/chunks/index.D_EU-tSc.js"];
export const stylesheets = [];
export const fonts = [];
