<script lang="ts">
	import ScreenCog from '$lib/assets/screenCog.svelte';
	import CloudIcon from '$lib/assets/maphealthicon.svelte';
	import GlassIcon from '$lib/assets/magglassicon.svelte';
	import { createForm } from 'felte';
	import * as yup from 'yup';
	import { writable } from 'svelte/store';
	import { enhance } from '$app/forms';
	import { error } from '@sveltejs/kit';
	let anchor = '';

	interface FormValues {
		name: string;
		email: string;
		message: string;
	}

	//Local state variables to sotre form data and errors
	let values: FormValues = { name: '', email: '', message: '' };
	let errors: Record<string, string> = {};

	//Yup Schema for validation
	const schema = yup.object({
		name: yup.string().required('Name is required'),
		email: yup.string().email('Invalid email address').required('Email is required'),
		message: yup.string().required('Message cannot be empty')
	});

	//Function to handle the form submission
	async function submitHandler(event: Event) {
		event.preventDefault();
		try {
			await schema.validate(values, { abortEarly: false });
			alert(JSON.stringify(values, null, 2));
			errors = {};
		} catch (err) {
			if (err instanceof yup.ValidationError) {
				errors = extractErrors(err);
			}
		}
	}

	//Function to extract errors
	function extractErrors(err: yup.ValidationError): Record<string, string> {
		return err.inner.reduce((acc, error) => {
			const path = error.path as string;
			return { ...acc, [path]: error.message };
		}, {});
	}

	function handleAnchorClick(event: { preventDefault: () => void; currentTarget: any }) {
		event.preventDefault();
		const link = event.currentTarget;
		const anchorId = new URL(link.href).hash.replace('#', '');
		const anchor = document.getElementById(anchorId);
		window.scrollTo({
			top: anchor?.offsetTop,
			behavior: 'smooth'
		});
	}
</script>

<header
	class="sticky top-0 z-10 shadow-sm bg-white bg-opacity-60 bg-clip-padding blur-backdrop-filter"
>
	<nav class="mx-auto flex items-center justify-between gap-x-6 p-6 lg:px-8" aria-label="Global">
		<div class="flex lg:flex-1">
			<a href="/" class="-m-1.5 p-1.5 text-nivaltaBlue font-bold text-3xl">Nivalta</a>
		</div>
		<div class="hidden lg:flex lg:gap-x-12">
			<a
				href="#home"
				on:click={handleAnchorClick}
				class="text-md font-semibold leading-6 text-gray-900 hover:text-nivaltaBlue">Home</a
			>
			<a
				href="#features"
				on:click={handleAnchorClick}
				class="text-md font-semibold leading-6 text-gray-900 hover:text-nivaltaBlue">Features</a
			>
			<a
				href="#about"
				on:click={handleAnchorClick}
				class="text-md font-semibold leading-6 text-gray-900 hover:text-nivaltaBlue">About Us</a
			>
			<a
				href="#contact"
				on:click={handleAnchorClick}
				class="text-md font-semibold leading-6 text-gray-900 hover:text-nivaltaBlue">Contact</a
			>
		</div>
		<div class="flex flex-1 items-center justify-end gap-x-6">
			<a
				href="#waitlist"
				on:click={handleAnchorClick}
				class="rounded-3xl bg-nivaltaBlue px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
				>Wait List</a
			>
		</div>
		<div class="flex lg:hidden">
			<button
				type="button"
				class="-m-2.5 inline-flex items-center justify-center rounded-md p-2.5 text-gray-700"
			>
				<span class="sr-only">Open main menu</span>
				<svg
					class="h-6 w-6"
					fill="none"
					viewBox="0 0 24 24"
					stroke-width="1.5"
					stroke="currentColor"
					aria-hidden="true"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5"
					/>
				</svg>
			</button>
		</div>
	</nav>

	<!-- Mobile menu, show/hide based on menu open state. -->
	<div class="lg:hidden" role="dialog" aria-modal="true">
		<!-- Background backdrop, show/hide based on slide-over state. -->
		<div class="fixed inset-0 z-10"></div>
		<div
			class="fixed inset-y-0 right-0 z-10 w-full overflow-y-auto bg-white px-6 py-6 sm:max-w-sm sm:ring-1 sm:ring-gray-900/10"
		>
			<div class="flex items-center gap-x-6">
				<a href="/" class="-m-1.5 p-1.5 text-nivaltaBlue font-bold text-3xl">Nivalta</a>
				<a
					href="/"
					class="ml-auto rounded-3xl bg-nivaltaBlue px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
					>Wait List</a
				>
				<button type="button" class="-m-2.5 rounded-md p-2.5 text-gray-700">
					<span class="sr-only">Close menu</span>
					<svg
						class="h-6 w-6"
						fill="none"
						viewBox="0 0 24 24"
						stroke-width="1.5"
						stroke="currentColor"
						aria-hidden="true"
					>
						<path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
					</svg>
				</button>
			</div>
			<div class="mt-6 flow-root">
				<div class="-my-6 divide-y divide-gray-500/10">
					<div class="space-y-2 py-6">
						<a
							href="/"
							class="-mx-3 block rounded-lg px-3 py-2 text-base font-semibold leading-7 text-gray-900 hover:bg-gray-50"
							>Home</a
						>
						<a
							href="/"
							class="-mx-3 block rounded-lg px-3 py-2 text-base font-semibold leading-7 text-gray-900 hover:bg-gray-50"
							>Features</a
						>
						<a
							href="/"
							class="-mx-3 block rounded-lg px-3 py-2 text-base font-semibold leading-7 text-gray-900 hover:bg-gray-50"
							>About Us</a
						>
						<a
							href="/"
							class="-mx-3 block rounded-lg px-3 py-2 text-base font-semibold leading-7 text-gray-900 hover:bg-gray-50"
							>Contact</a
						>
					</div>
					<!--             <div class="py-6">
                <a href="/" class="-mx-3 block rounded-lg px-3 py-2.5 text-base font-semibold leading-7 text-gray-900 hover:bg-gray-50">Wait List</a>
            </div> -->
				</div>
			</div>
		</div>
	</div>
</header>

<main class="isolate bg-white flex flex-col min-h-screen">
	<!-- Hero Section -->
	<div id="home" class="relative isolate overflow-hidden bg-white">
		<svg
			class="absolute inset-0 -z-10 h-full w-full stroke-gray-200 [mask-image:radial-gradient(100%_100%_at_top_right,white,transparent)]"
			aria-hidden="true"
		>
			<defs>
				<pattern
					id="0787a7c5-978c-4f66-83c7-11c213f99cb7"
					width="200"
					height="200"
					x="50%"
					y="-1"
					patternUnits="userSpaceOnUse"
				>
					<path d="M.5 200V.5H200" fill="none" />
				</pattern>
			</defs>
			<rect
				width="100%"
				height="100%"
				stroke-width="0"
				fill="url(#0787a7c5-978c-4f66-83c7-11c213f99cb7)"
			/>
		</svg>
		<div class="mx-auto max-w-7xl px-6 pb-24 pt-10 sm:pb-32 lg:flex lg:px-8 lg:py-40">
			<div class="mx-auto max-w-2xl lg:mx-0 lg:max-w-xl lg:flex-shrink-0 lg:pt-8">
				<div class="mt-24 sm:mt-32 lg:mt-16">
					<a href="/" class="inline-flex space-x-6"> </a>
				</div>
				<h1 class="mt-10 text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">
					Transform your health data into personalized insights
				</h1>
				<p class="mt-6 text-lg leading-8 text-gray-600">
					Seamlessly combine your health records, symptoms, habits, and history to unlock
					personalized wellness strategies.
				</p>
				<div class="mt-10 flex items-center gap-x-6">
					<a
						href="#waitlist"
						on:click={handleAnchorClick}
						class="rounded-3xl bg-nivaltaBlue px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
						>Wait List</a
					>
					<a
						href="#features"
						on:click={handleAnchorClick}
						class="text-sm font-semibold leading-6 text-gray-900"
						>Learn more <span aria-hidden="true">→</span></a
					>
				</div>
			</div>
			<div
				class="mx-auto mt-16 flex max-w-2xl sm:mt-24 lg:ml-10 lg:mr-0 lg:mt-0 lg:max-w-none lg:flex-none xl:ml-32"
			>
				<div class="max-w-3xl flex-none sm:max-w-5xl lg:max-w-none">
					<div
						class="-m-2 rounded-xl bg-gray-900/5 p-2 ring-1 ring-inset ring-gray-900/10 lg:-m-4 lg:rounded-2xl lg:p-4"
					>
						<img
							src="https://tailwindui.com/plus/img/component-images/project-app-screenshot.png"
							alt="App screenshot"
							width="2432"
							height="1442"
							class="w-[76rem] rounded-md shadow-2xl ring-1 ring-gray-900/10"
						/>
					</div>
				</div>
			</div>
		</div>
	</div>

	<!-- Features Section -->
	<div id="features" class="relative isolate overflow-hidden bg-white py-24 sm:py-32">
		<div
			class="hidden sm:absolute sm:-top-10 sm:right-1/2 sm:-z-10 sm:mr-10 sm:block sm:transform-gpu sm:blur-3xl"
		>
			<div
				class="aspect-[1097/845] w-[68.5625rem] bg-gradient-to-tr from-[#ff4694] to-[#776fff] opacity-20"
				style="clip-path: polygon(74.1% 44.1%, 100% 61.6%, 97.5% 26.9%, 85.5% 0.1%, 80.7% 2%, 72.5% 32.5%, 60.2% 62.4%, 52.4% 68.1%, 47.5% 58.3%, 45.2% 34.5%, 27.5% 76.7%, 0.1% 64.9%, 17.9% 100%, 27.6% 76.8%, 76.1% 97.7%, 74.1% 44.1%)"
			></div>
		</div>
		<div
			class="absolute -top-52 left-1/2 -z-10 -translate-x-1/2 transform-gpu blur-3xl sm:top-[-28rem] sm:ml-16 sm:translate-x-0 sm:transform-gpu"
		>
			<div
				class="aspect-[1097/845] w-[68.5625rem] bg-gradient-to-tr from-[#ff4694] to-[#776fff] opacity-20"
				style="clip-path: polygon(74.1% 44.1%, 100% 61.6%, 97.5% 26.9%, 85.5% 0.1%, 80.7% 2%, 72.5% 32.5%, 60.2% 62.4%, 52.4% 68.1%, 47.5% 58.3%, 45.2% 34.5%, 27.5% 76.7%, 0.1% 64.9%, 17.9% 100%, 27.6% 76.8%, 76.1% 97.7%, 74.1% 44.1%)"
			></div>
		</div>
		<div class="mx-auto max-w-7xl px-6 lg:px-8">
			<div class="mx-auto max-w-2xl lg:mx-0">
				<h2 class="text-4xl font-bold tracking-tight text-grey-900 sm:text-6xl">
					Your Complete Health Management Tool Kit
				</h2>
			</div>
			<div
				class="mx-auto mt-16 grid max-w-2xl grid-cols-1 gap-6 sm:mt-20 lg:mx-0 lg:max-w-none lg:grid-cols-4 lg:gap-8"
			>
				<div class="flex-col gap-x-4 rounded-xl bg-white/5 p-6 ring-1 ring-inset ring-white/10">
					<div class="h-14 w-12">
						<ScreenCog />
					</div>
					<div class="text-base leading-7">
						<h3 class="font-semibold text-grey-900">Upload & Integrate</h3>
						<p class="mt-3 text-grey-900 block">
							Upload and consolidate health data from various sources into one secure profile.
						</p>
					</div>
				</div>
				<div class="flex-col gap-x-4 rounded-xl bg-white/5 p-6 ring-1 ring-inset ring-white/10">
					<div class="h-14 w-12">
						<ScreenCog />
					</div>
					<div class="text-base leading-7">
						<h3 class="font-semibold ttext-grey-900">Track Your Symptoms</h3>
						<p class="mt-3 text-grey-900">
							Log symptoms, identify problems, and generate reports for heatlhcare providers.
						</p>
					</div>
				</div>
				<div class="flex-col gap-x-4 rounded-xl bg-white/5 p-6 ring-1 ring-inset ring-white/10">
					<div class="h-14 w-12">
						<CloudIcon />
					</div>
					<div class="text-base leading-7">
						<h3 class="font-semibold text-grey-900">Map Family Health</h3>
						<p class="mt-3 text-grey-900">
							Create your family heatlh tree to better understand genetic predispositions and risks.
						</p>
					</div>
				</div>
				<div class="flex-col gap-x-4 rounded-xl bg-white/5 p-6 ring-1 ring-inset ring-white/10">
					<div class="h-14 w-12">
						<GlassIcon />
					</div>
					<div class="text-base leading-7">
						<h3 class="font-semibold text-grey-900">Discover Health Insights</h3>
						<p class="mt-3 text-grey-900">
							Get tailored analysis and actionable recommendations for your wellness.
						</p>
					</div>
				</div>
			</div>
		</div>
	</div>

	<!-- About Us Section -->
	<div id="about" class="relative bg-white">
		<div class="mx-auto max-w-7xl lg:flex lg:justify-between lg:px-8 xl:justify-end">
			<div
				class="lg:flex lg:w-1/2 lg:shrink lg:grow-0 xl:absolute xl:inset-y-0 xl:right-1/2 xl:w-1/2"
			>
				<div class="relative h-80 lg:-ml-8 lg:h-auto lg:w-full lg:grow xl:ml-0">
					<img
						class="absolute inset-0 h-full w-full bg-gray-50 object-cover"
						src="https://images.unsplash.com/photo-1559136555-9303baea8ebd?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&crop=focalpoint&fp-x=.4&w=2560&h=3413&&q=80"
						alt=""
					/>
				</div>
			</div>
			<div class="px-6 lg:contents">
				<div
					class="mx-auto max-w-2xl pb-24 pt-16 sm:pb-32 sm:pt-20 lg:ml-8 lg:mr-0 lg:w-full lg:max-w-lg lg:flex-none lg:pt-32 xl:w-1/2"
				>
					<h1 class="mt-2 text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
						Pioneering the future of personalized health management.
					</h1>
					<p class="mt-6 text-xl leading-8 text-gray-700">
						We transform complex health information into clear, actionable insights tailored to your
						individual health profile.
					</p>
					<div class="mt-10 max-w-xl text-base leading-7 text-gray-700 lg:max-w-none">
						<p>
							We aim to empower individuals with tools and information readily accessible about
							their individual health. Our tools work for you to assist you with getting to the
							bottom of your health care issues, have powerful analysis tools such as artificial
							intellgence and visual graphs. Whether you are on the go and need to quickly log
							symptoms or have time to dig deeper, we have the tools to help unlock insights that
							were previously undiscovered.
						</p>
						<ul role="list" class="mt-8 space-y-8 text-gray-600">
							<li class="flex gap-x-3">
								<svg
									class="mt-1 h-5 w-5 flex-none text-nivaltaBlue"
									viewBox="0 0 20 20"
									fill="currentColor"
									aria-hidden="true"
									data-slot="icon"
								>
									<path
										fill-rule="evenodd"
										d="M5.5 17a4.5 4.5 0 0 1-1.44-8.765 4.5 4.5 0 0 1 8.302-3.046 3.5 3.5 0 0 1 4.504 4.272A4 4 0 0 1 15 17H5.5Zm3.75-2.75a.75.75 0 0 0 1.5 0V9.66l1.95 2.1a.75.75 0 1 0 1.1-1.02l-3.25-3.5a.75.75 0 0 0-1.1 0l-3.25 3.5a.75.75 0 1 0 1.1 1.02l1.95-2.1v4.59Z"
										clip-rule="evenodd"
									/>
								</svg>
								<span
									><strong class="font-semibold text-gray-900">Upload Health Records.</strong> Nivalta
									health wants to leverage technology to make your life easier; uploading health records
									such as office visits, dignostics, or even lab results. Our aim is to consolidate your
									entire health record into one place to fit your needs.</span
								>
							</li>
							<li class="flex gap-x-3">
								<svg
									class="mt-1 h-5 w-5 flex-none text-nivaltaBlue"
									viewBox="0 0 20 20"
									fill="currentColor"
									aria-hidden="true"
									data-slot="icon"
								>
									<path
										fill-rule="evenodd"
										d="M10 1a4.5 4.5 0 0 0-4.5 4.5V9H5a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-6a2 2 0 0 0-2-2h-.5V5.5A4.5 4.5 0 0 0 10 1Zm3 8V5.5a3 3 0 1 0-6 0V9h6Z"
										clip-rule="evenodd"
									/>
								</svg>
								<span
									><strong class="font-semibold text-gray-900">Data Security</strong> Truly our health
									records are sensitive information to us. At Nivalta, we encrypt everything you upload
									or add to our services giving you confidence in our tools. You can delete anything
									you desire giving you full control of experience with Nivalta.</span
								>
							</li>
							<li class="flex gap-x-3">
								<svg
									class="mt-1 h-5 w-5 flex-none text-nivaltaBlue"
									viewBox="0 0 20 20"
									fill="currentColor"
									aria-hidden="true"
									data-slot="icon"
								>
									<path
										d="M4.632 3.533A2 2 0 0 1 6.577 2h6.846a2 2 0 0 1 1.945 1.533l1.976 8.234A3.489 3.489 0 0 0 16 11.5H4c-.476 0-.93.095-1.344.267l1.976-8.234Z"
									/>
									<path
										fill-rule="evenodd"
										d="M4 13a2 2 0 1 0 0 4h12a2 2 0 1 0 0-4H4Zm11.24 2a.75.75 0 0 1 .75-.75H16a.75.75 0 0 1 .75.75v.01a.75.75 0 0 1-.75.75h-.01a.75.75 0 0 1-.75-.75V15Zm-2.25-.75a.75.75 0 0 0-.75.75v.01c0 .414.336.75.75.75H13a.75.75 0 0 0 .75-.75V15a.75.75 0 0 0-.75-.75h-.01Z"
										clip-rule="evenodd"
									/>
								</svg>
								<span
									><strong class="font-semibold text-gray-900">Data Mobility.</strong> Whether you have
									moved across the country or simply changed healthcare providers, Nivalta allows you
									to take your insights and records with you.
								</span>
							</li>
						</ul>
						<h2 class="mt-16 text-2xl font-bold tracking-tight text-gray-900">
							No Computer? No Problem.
						</h2>
						<p class="mt-6">
							Our mobile app is just as powerful and when you are often on the go, we still want you
							to have access to our tools. We understand you might not have the ability to track a
							sympton while you are on the move and when time is of the essence, our mobile app will
							capture your symptoms or data so you can carry on with your day.
						</p>
						<p class="text-base font-semibold leading-7 text-nivaltaBlue">Coming Soon</p>
					</div>
				</div>
			</div>
		</div>
	</div>

	<!-- Content section -->
	<div class="mt-32 overflow-hidden sm:mt-40 bg-white">
		<div class="mx-auto max-w-7xl px-6 lg:flex lg:px-8">
			<div
				class="mx-auto grid max-w-2xl grid-cols-1 gap-x-12 gap-y-16 lg:mx-0 lg:min-w-full lg:max-w-none lg:flex-none lg:gap-y-8"
			>
				<div class="lg:col-end-1 lg:w-full lg:max-w-lg lg:pb-8">
					<h2 class="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">Our people</h2>
					<p class="mt-6 text-xl leading-8 text-gray-600">
						Our staff here at Nivalta all have a personal attachment to this company's mission. We
						care about being in control of our healthcare and want to share that with others like
						you.
					</p>
					<p class="mt-6 text-base leading-7 text-gray-600">
						Nivalta also cares about empowering medical providers with having all the necessary data
						they can possibly have about an individual to assess and diagnose. Getting back to their
						passion for healthcare. Nivalta tools are meant to enhance medical providers work by
						serving them data to make diagnotics as efficient as possible.
					</p>
				</div>
				<div class="flex flex-wrap items-start justify-end gap-6 sm:gap-8 lg:contents">
					<div class="w-0 flex-auto lg:ml-auto lg:w-auto lg:flex-none lg:self-end">
						<img
							src="https://images.unsplash.com/photo-1670272502246-768d249768ca?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1152&q=80"
							alt=""
							class="aspect-[7/5] w-[37rem] max-w-none rounded-2xl bg-gray-50 object-cover"
						/>
					</div>
					<div
						class="contents lg:col-span-2 lg:col-end-2 lg:ml-auto lg:flex lg:w-[37rem] lg:items-start lg:justify-end lg:gap-x-8"
					>
						<div class="order-first flex w-64 flex-none justify-end self-end lg:w-auto">
							<img
								src="https://images.unsplash.com/photo-1605656816944-971cd5c1407f?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=768&h=604&q=80"
								alt=""
								class="aspect-[4/3] w-[24rem] max-w-none flex-none rounded-2xl bg-gray-50 object-cover"
							/>
						</div>
						<div class="flex w-96 flex-auto justify-end lg:w-auto lg:flex-none">
							<img
								src="https://images.unsplash.com/photo-1568992687947-868a62a9f521?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1152&h=842&q=80"
								alt=""
								class="aspect-[7/5] w-[37rem] max-w-none flex-none rounded-2xl bg-gray-50 object-cover"
							/>
						</div>
						<div class="hidden sm:block sm:w-0 sm:flex-auto lg:w-auto lg:flex-none">
							<img
								src="https://images.unsplash.com/photo-1612872087720-bb876e2e67d1?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=768&h=604&q=80"
								alt=""
								class="aspect-[4/3] w-[24rem] max-w-none rounded-2xl bg-gray-50 object-cover"
							/>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>

	<!-- Contact Us Section -->
	<div id="contact" class="relative isolate px-6 py-24 sm:py-32 lg:px-8">
		<div class="mx-auto max-w-xl lg:max-w-4xl">
			<h2 class="text-4xl font-bold tracking-tight text-gray-900">Looking for more information?</h2>
			<p class="mt-2 text-lg leading-8 text-gray-600">
				We are here to help in anyway. Simply fill out our form below and we will have someone
				contact you promptly.
			</p>
			<div class="mt-16 flex flex-col gap-16 sm:gap-y-20 lg:flex-row">
				<form on:submit|preventDefault={submitHandler} novalidate class="lg:flex-auto">
					<div class="grid grid-cols-1 gap-x-8 gap-y-6 sm:grid-cols-2">
						<div>
							<label for="first-name" class="block text-sm font-semibold leading-6 text-gray-900"
								>Name</label
							>
							<div class="mt-2.5">
								<input
									type="text"
									name="name"
									id="name"
									bind:value={values.name}
									placeholder="Enter your name"
									class="block w-full rounded-md border-0 px-3.5 py-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
								/>
								{#if errors.name}
									<p class="text-red-500 text-sm mt-1">{errors.name}</p>
								{/if}
							</div>
						</div>
						<div>
							<label for="last-name" class="block text-sm font-semibold leading-6 text-gray-900"
								>Email</label
							>
							<div class="mt-2.5">
								<input
									type="text"
									id="email"
									bind:value={values.email}
									placeholder="Your email address"
									class="block w-full rounded-md border-0 px-3.5 py-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
								/>
								{#if errors.name}
									<p class="text-red-500 text-sm mt-1">{errors.email}</p>
								{/if}
							</div>
						</div>
						<div class="sm:col-span-2">
							<label for="message" class="block text-sm font-semibold leading-6 text-gray-900"
								>Message</label
							>
							<div class="mt-2.5">
								<textarea
									id="message"
									bind:value={values.message}
									rows="4"
									class="block w-full rounded-md border-0 px-3.5 py-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
								></textarea>
								{#if errors.name}
									<p class="text-red-500 text-sm mt-1">{errors.message}</p>
								{/if}
							</div>
						</div>
					</div>
					<div class="mt-10">
						<button
							type="submit"
							class="block w-full rounded-md bg-nivaltaBlue px-3.5 py-2.5 text-center text-sm font-semibold text-white shadow-sm hover:bg-indigo-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
							>Let’s talk</button
						>
					</div>
					<p class="mt-4 text-sm leading-6 text-gray-500">
						By submitting this form, I agree to the <a
							href="/"
							class="font-semibold text-nivaltaBlue">privacy&nbsp;policy</a
						>.
					</p>
				</form>
				<div class="lg:mt-6 lg:w-80 lg:flex-none">
					<figure class="mt-2">
						<blockquote class="text-lg font-semibold leading-8 text-gray-900">
							<p>
								“I have been passionate about knowing more about my health through tracking data and
								seeing trends in my own lab work. I hope to bring that same passion for healthcare
								data to individuals and doctors alike.”
							</p>
						</blockquote>
						<figcaption class="mt-10 flex gap-x-6">
							<img
								src="https://images.unsplash.com/photo-1550525811-e5869dd03032?ixlib=rb-=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=96&h=96&q=80"
								alt=""
								class="h-12 w-12 flex-none rounded-full bg-gray-50"
							/>
							<div>
								<div class="text-base font-semibold text-gray-900">Madeleine Trudeau</div>
								<div class="text-sm leading-6 text-gray-600">CEO of Nivalta</div>
							</div>
						</figcaption>
					</figure>
				</div>
			</div>
		</div>
	</div>
</main>

<!-- Footer --->
<footer id="waitlist" class="bg-gray-900 mt-auto" aria-labelledby="footer-heading">
	<h2 id="footer-heading" class="sr-only">Footer</h2>
	<div class="mx-auto max-w-7xl px-6 pb-8 pt-8 sm:pt-24 lg:px-8 lg:pt-8">
		<div class="xl:grid xl:grid-cols-3 xl:gap-8"></div>
		<div
			class="mt-8 border-t border-white/10 pt-4 pb-4 sm:mt-20 lg:mt-6 lg:flex lg:items-center lg:justify-between"
		>
			<div class="">
				<h3 class="text-sm font-semibold leading-6 text-white">Sign up today</h3>
				<p class="mt-2 text-sm leading-6 text-gray-300">
					Join our waitlist to be the first to hear about new features and updates. We promise not
					to send any junk.
				</p>
			</div>
			<form
				use:enhance
				method="POST"
				class="mt-6 sm:flex sm:max-w-md lg:mt-0"
				on:submit={submitHandler}
			>
				<label for="email-address" class="sr-only">Email address</label>
				<input
					type="email"
					name="email-address"
					id="email-address"
					class="w-full min-w-0 appearance-none rounded-md border-0 bg-white/5 px-3 py-1.5 text-base text-white shadow-sm ring-1 ring-inset ring-white/10 placeholder:text-gray-500 focus:ring-2 focus:ring-inset focus:ring-indigo-500 sm:w-56 sm:text-sm sm:leading-6"
					placeholder="Enter your email"
				/>
				<div class="mt-4 sm:ml-4 sm:mt-0 sm:flex-shrink-0">
					<button
						type="submit"
						class="flex w-full items-center justify-center rounded-3xl bg-nivaltaBlue px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
						>Wait List</button
					>
				</div>
			</form>
		</div>
		<div class="border-t border-white/10 pt-4 md:flex md:items-center md:justify-between">
			<p class="text-xs leading-5 text-gray-400 md:order-1 md:mt-0">
				&copy; 2024 Nivalta, Inc. All rights reserved.
			</p>
		</div>
	</div>
</footer>

<style>
	.blur-backdrop-filter {
		backdrop-filter: blur(5px);
		-webkit-backdrop-filter: blur(5px);
	}
</style>
