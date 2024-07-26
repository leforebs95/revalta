

export const index = 5;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/_user_/_page.svelte.js')).default;
export const imports = ["_app/immutable/nodes/5.R1my0Oh3.js","_app/immutable/chunks/scheduler.Bmg8oFKD.js","_app/immutable/chunks/index.B7858mxG.js"];
export const stylesheets = [];
export const fonts = [];
