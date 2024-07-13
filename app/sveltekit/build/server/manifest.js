const manifest = (() => {
function __memo(fn) {
	let value;
	return () => value ??= (value = fn());
}

return {
	appDir: "_app",
	appPath: "_app",
	assets: new Set(["favicon.png","images/hero.svg"]),
	mimeTypes: {".png":"image/png",".svg":"image/svg+xml"},
	_: {
		client: {"start":"_app/immutable/entry/start.D0MOY0Q8.js","app":"_app/immutable/entry/app.CrFpyPIl.js","imports":["_app/immutable/entry/start.D0MOY0Q8.js","_app/immutable/chunks/entry.C1fxw7XC.js","_app/immutable/chunks/scheduler.Bmg8oFKD.js","_app/immutable/chunks/index.D_GRTHN4.js","_app/immutable/entry/app.CrFpyPIl.js","_app/immutable/chunks/scheduler.Bmg8oFKD.js","_app/immutable/chunks/index.D_EU-tSc.js"],"stylesheets":[],"fonts":[],"uses_env_dynamic_public":false},
		nodes: [
			__memo(() => import('./chunks/0-BZkAG6kk.js')),
			__memo(() => import('./chunks/1-Bs4P0ypb.js')),
			__memo(() => import('./chunks/2-DHIQc0i9.js')),
			__memo(() => import('./chunks/3-wrZLe659.js')),
			__memo(() => import('./chunks/4-B7LPRrbz.js')),
			__memo(() => import('./chunks/5-CEKfgGow.js'))
		],
		routes: [
			{
				id: "/",
				pattern: /^\/$/,
				params: [],
				page: { layouts: [0,], errors: [1,], leaf: 2 },
				endpoint: null
			},
			{
				id: "/login/forgotpassword",
				pattern: /^\/login\/forgotpassword\/?$/,
				params: [],
				page: { layouts: [0,], errors: [1,], leaf: 4 },
				endpoint: null
			},
			{
				id: "/login/signup",
				pattern: /^\/login\/signup\/?$/,
				params: [],
				page: { layouts: [0,], errors: [1,], leaf: 5 },
				endpoint: null
			},
			{
				id: "/[user]",
				pattern: /^\/([^/]+?)\/?$/,
				params: [{"name":"user","optional":false,"rest":false,"chained":false}],
				page: { layouts: [0,], errors: [1,], leaf: 3 },
				endpoint: null
			}
		],
		matchers: async () => {
			
			return {  };
		},
		server_assets: {}
	}
}
})();

const prerendered = new Set([]);

const base = "";

export { base, manifest, prerendered };
//# sourceMappingURL=manifest.js.map
