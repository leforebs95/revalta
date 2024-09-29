<script lang="ts">
  let anchor = '';

  function handleAnchorClick (event: { preventDefault: () => void; currentTarget: any; }) {
    event.preventDefault()
    const link = event.currentTarget
    const anchorId = new URL(link.href).hash.replace('#', '')
    const anchor = document.getElementById(anchorId)
    window.scrollTo({
      top: anchor?.offsetTop,
      behavior: 'smooth'
    })
  }
</script>

<header class="bg-white">
  <nav class="mx-auto flex items-center justify-between gap-x-6 p-6 lg:px-8" aria-label="Global">
      <div class="flex lg:flex-1">
      <a href="/" class="-m-1.5 p-1.5 text-nivaltaBlue font-bold text-3xl">Nivalta</a>
      </div>
      <div class="hidden lg:flex lg:gap-x-12">
      <a href="/" class="text-md font-semibold leading-6 text-gray-900">Home</a>
      <a href="#features" on:click={handleAnchorClick} class="text-md font-semibold leading-6 text-gray-900">Features</a>
      <a href="#about" on:click={handleAnchorClick} class="text-md font-semibold leading-6 text-gray-900">About Us</a>
      <a href="#contact" on:click={handleAnchorClick} class="text-md font-semibold leading-6 text-gray-900">Contact</a>
      </div>
      <div class="flex flex-1 items-center justify-end gap-x-6">
      <a href="#waitlist" on:click={handleAnchorClick} class="rounded-3xl bg-nivaltaBlue px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">Wait List</a>
      </div>
      <div class="flex lg:hidden">
      <button type="button" class="-m-2.5 inline-flex items-center justify-center rounded-md p-2.5 text-gray-700">
          <span class="sr-only">Open main menu</span>
          <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" aria-hidden="true">
          <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
          </svg>
      </button>
      </div>
  </nav>

  <!-- Mobile menu, show/hide based on menu open state. -->
  <div class="lg:hidden" role="dialog" aria-modal="true">
      <!-- Background backdrop, show/hide based on slide-over state. -->
      <div class="fixed inset-0 z-10"></div>
      <div class="fixed inset-y-0 right-0 z-10 w-full overflow-y-auto bg-white px-6 py-6 sm:max-w-sm sm:ring-1 sm:ring-gray-900/10">
      <div class="flex items-center gap-x-6">
          <a href="/" class="-m-1.5 p-1.5 text-nivaltaBlue font-bold text-3xl">Nivalta</a>
          <a href="/" class="ml-auto rounded-3xl bg-nivaltaBlue px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">Wait List</a>
          <button type="button" class="-m-2.5 rounded-md p-2.5 text-gray-700">
          <span class="sr-only">Close menu</span>
          <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
          </svg>
          </button>
      </div>
      <div class="mt-6 flow-root">
          <div class="-my-6 divide-y divide-gray-500/10">
          <div class="space-y-2 py-6">
              <a href="/" class="-mx-3 block rounded-lg px-3 py-2 text-base font-semibold leading-7 text-gray-900 hover:bg-gray-50">Home</a>
              <a href="/" class="-mx-3 block rounded-lg px-3 py-2 text-base font-semibold leading-7 text-gray-900 hover:bg-gray-50">Features</a>
              <a href="/" class="-mx-3 block rounded-lg px-3 py-2 text-base font-semibold leading-7 text-gray-900 hover:bg-gray-50">About Us</a>
              <a href="/" class="-mx-3 block rounded-lg px-3 py-2 text-base font-semibold leading-7 text-gray-900 hover:bg-gray-50">Contact</a>
          </div>
          <!-- <div class="py-6">
              <a href="/" class="-mx-3 block rounded-lg px-3 py-2.5 text-base font-semibold leading-7 text-gray-900 hover:bg-gray-50">Wait List</a>
          </div> -->
          </div>
      </div>
      </div>
  </div>
</header>

<main class="isolate bg-slate-100">
          
  <!-- Hero Section -->
  <div class="relative isolate overflow-hidden bg-white">
    <svg class="absolute inset-0 -z-10 h-full w-full stroke-gray-200 [mask-image:radial-gradient(100%_100%_at_top_right,white,transparent)]" aria-hidden="true">
      <defs>
        <pattern id="0787a7c5-978c-4f66-83c7-11c213f99cb7" width="200" height="200" x="50%" y="-1" patternUnits="userSpaceOnUse">
          <path d="M.5 200V.5H200" fill="none" />
        </pattern>
      </defs>
      <rect width="100%" height="100%" stroke-width="0" fill="url(#0787a7c5-978c-4f66-83c7-11c213f99cb7)" />
    </svg>
    <div class="mx-auto max-w-7xl px-6 pb-24 pt-10 sm:pb-32 lg:flex lg:px-8 lg:py-40">
      <div class="mx-auto max-w-2xl lg:mx-0 lg:max-w-xl lg:flex-shrink-0 lg:pt-8">
        <div class="mt-24 sm:mt-32 lg:mt-16">
          <a href="/" class="inline-flex space-x-6">
          </a>
        </div>
        <h1 class="mt-10 text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">Transform your health data into personalized insights</h1>
        <p class="mt-6 text-lg leading-8 text-gray-600">Seamlessly combine your health records, symptoms, habits, and history to unlock personalized wellness strategies.</p>
        <div class="mt-10 flex items-center gap-x-6">
          <a href="#waitlist" on:click={handleAnchorClick} class="rounded-3xl bg-nivaltaBlue px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">Wait List</a>
          <a href="#features" on:click={handleAnchorClick} class="text-sm font-semibold leading-6 text-gray-900">Learn more <span aria-hidden="true">→</span></a>
        </div>
      </div>
      <div class="mx-auto mt-16 flex max-w-2xl sm:mt-24 lg:ml-10 lg:mr-0 lg:mt-0 lg:max-w-none lg:flex-none xl:ml-32">
        <div class="max-w-3xl flex-none sm:max-w-5xl lg:max-w-none">
          <div class="-m-2 rounded-xl bg-gray-900/5 p-2 ring-1 ring-inset ring-gray-900/10 lg:-m-4 lg:rounded-2xl lg:p-4">
            <img src="https://tailwindui.com/img/component-images/project-app-screenshot.png" alt="App screenshot" width="2432" height="1442" class="w-[76rem] rounded-md shadow-2xl ring-1 ring-gray-900/10">
          </div>
        </div>
      </div>
    </div>
  </div>  
     
  <!-- Features Section -->  
  <div id="features" class="bg-gray-50 pt-12 sm:pt-16">
    <div class="mx-auto max-w-7xl px-6 lg:px-8">
      <div class="mx-auto max-w-4xl text-center">
        <h2 class="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">Your Complete Health Management Toolkit</h2>
      </div>
    </div>
    <div class="mt-10 bg-white pb-12 sm:pb-16">
      <div class="relative">
        <div class="absolute inset-0 h-1/2 bg-gray-50"></div>
        <div class="relative mx-auto max-w-10xl px-6 lg:px-8">
          <div class="mx-auto max-w-6xl">
            <ul role="list" class="grid grid-cols-1 gap-6 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
              <li class="col-span-1 flex flex-col divide-y divide-gray-200 rounded-lg bg-white text-center shadow">
                <div class="flex flex-1 flex-col p-8">
                  <img class="mx-auto h-32 w-32 flex-shrink-0 rounded-full" src="https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=4&w=256&h=256&q=60" alt="">
                  <h3 class="mt-6 text-sm font-medium text-gray-900">Jane Cooper</h3>
                  <dl class="mt-1 flex flex-grow flex-col justify-between">
                    <dt class="sr-only">Title</dt>
                    <dd class="text-sm text-gray-500">Paradigm Representative</dd>
                    <dt class="sr-only">Role</dt>
                    <dd class="mt-3">
                      <span class="inline-flex items-center rounded-full bg-green-50 px-2 py-1 text-xs font-medium text-green-700 ring-1 ring-inset ring-green-600/20">Admin</span>
                    </dd>
                  </dl>
                </div>
                <div>
                  <div class="-mt-px flex divide-x divide-gray-200">
                    <div class="flex w-0 flex-1">
                      <a href="mailto:janecooper@example.com" class="relative -mr-px inline-flex w-0 flex-1 items-center justify-center gap-x-3 rounded-bl-lg border border-transparent py-4 text-sm font-semibold text-gray-900">
                        <svg class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                          <path d="M3 4a2 2 0 00-2 2v1.161l8.441 4.221a1.25 1.25 0 001.118 0L19 7.162V6a2 2 0 00-2-2H3z" />
                          <path d="M19 8.839l-7.77 3.885a2.75 2.75 0 01-2.46 0L1 8.839V14a2 2 0 002 2h14a2 2 0 002-2V8.839z" />
                        </svg>
                        Email
                      </a>
                    </div>
                    <div class="-ml-px flex w-0 flex-1">
                      <a href="tel:+1-202-555-0170" class="relative inline-flex w-0 flex-1 items-center justify-center gap-x-3 rounded-br-lg border border-transparent py-4 text-sm font-semibold text-gray-900">
                        <svg class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                          <path fill-rule="evenodd" d="M2 3.5A1.5 1.5 0 013.5 2h1.148a1.5 1.5 0 011.465 1.175l.716 3.223a1.5 1.5 0 01-1.052 1.767l-.933.267c-.41.117-.643.555-.48.95a11.542 11.542 0 006.254 6.254c.395.163.833-.07.95-.48l.267-.933a1.5 1.5 0 011.767-1.052l3.223.716A1.5 1.5 0 0118 15.352V16.5a1.5 1.5 0 01-1.5 1.5H15c-1.149 0-2.263-.15-3.326-.43A13.022 13.022 0 012.43 8.326 13.019 13.019 0 012 5V3.5z" clip-rule="evenodd" />
                        </svg>
                        Call
                      </a>
                    </div>
                  </div>
                </div>
              </li>
            
              <!-- More people... -->
            </ul>

            
            <!-- <dl class="rounded-lg bg-white shadow-lg sm:grid sm:grid-cols-3">
              <div class="flex flex-col border-b border-gray-100 p-6 text-center sm:border-0 sm:border-r">
                <dt class="order-2 mt-2 text-lg font-medium leading-6 text-gray-500">Upload & Integrate</dt>
                <p class="text-sm text-gray-500">Upload and consolidate health data from various sources into one secure profile.</p>
                <dd class="order-1 text-5xl font-bold tracking-tight text-indigo-600">100%</dd>
              </div>
              <div class="flex flex-col border-b border-t border-gray-100 p-6 text-center sm:border-0 sm:border-l sm:border-r">
                <dt class="order-2 mt-2 text-lg font-medium leading-6 text-gray-500">Delivery</dt>
                <dd class="order-1 text-5xl font-bold tracking-tight text-indigo-600">24/7</dd>
              </div>
              <div class="flex flex-col border-t border-gray-100 p-6 text-center sm:border-0 sm:border-l">
                <dt class="order-2 mt-2 text-lg font-medium leading-6 text-gray-500">Calories</dt>
                <dd class="order-1 text-5xl font-bold tracking-tight text-indigo-600">100k</dd>
              </div>
              <div class="flex flex-col border-t border-gray-100 p-6 text-center sm:border-0 sm:border-l">
                <dt class="order-2 mt-2 text-lg font-medium leading-6 text-gray-500">Calories</dt>
                <dd class="order-1 text-5xl font-bold tracking-tight text-indigo-600">100k</dd>
              </div>
            </dl> -->
          </div>
        </div>
      </div>
    </div>
  </div>
  
  <!-- About Us Section -->
  <div id="about" class="relative isolate -z-10 overflow-hidden bg-gradient-to-b from-indigo-100/20 pt-14">
      <div class="absolute inset-y-0 right-1/2 -z-10 -mr-96 w-[200%] origin-top-right skew-x-[-30deg] bg-white shadow-xl shadow-indigo-600/10 ring-1 ring-indigo-50 sm:-mr-80 lg:-mr-96" aria-hidden="true"></div>
      <div class="mx-auto max-w-7xl px-6 py-32 sm:py-40 lg:px-8">
        <div class="mx-auto max-w-2xl lg:mx-0 lg:grid lg:max-w-none lg:grid-cols-2 lg:gap-x-16 lg:gap-y-6 xl:grid-cols-1 xl:grid-rows-1 xl:gap-x-8">
          <h1 class="max-w-2xl text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl lg:col-span-2 xl:col-auto">We’re a passionate group of people working from around the world to build the future of ecommerce.</h1>
          <div class="mt-6 max-w-xl lg:mt-0 xl:col-end-1 xl:row-start-1">
            <p class="text-lg leading-8 text-gray-600">Anim aute id magna aliqua ad ad non deserunt sunt. Qui irure qui lorem cupidatat commodo. Elit sunt amet fugiat veniam occaecat fugiat aliqua. Anim aute id magna aliqua ad ad non deserunt sunt. Qui irure qui lorem cupidatat commodo.</p>
          </div>
          <img src="https://images.unsplash.com/photo-1567532900872-f4e906cbf06a?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1280&q=80" alt="" class="mt-10 aspect-[6/5] w-full max-w-lg rounded-2xl object-cover sm:mt-16 lg:mt-0 lg:max-w-none xl:row-span-2 xl:row-end-2 xl:mt-36">
        </div>
      </div>
      <div class="absolute inset-x-0 bottom-0 -z-10 h-24 bg-gradient-to-t from-white sm:h-32"></div>
    </div>

    <!-- Timeline section -->
    <div class="mx-auto -mt-8 max-w-7xl px-6 lg:px-8">
      <div class="mx-auto grid max-w-2xl grid-cols-1 gap-8 overflow-hidden lg:mx-0 lg:max-w-none lg:grid-cols-4">
        <div>
          <time datetime="2021-08" class="flex items-center text-sm font-semibold leading-6 text-indigo-600">
            <svg viewBox="0 0 4 4" class="mr-4 h-1 w-1 flex-none" aria-hidden="true">
              <circle cx="2" cy="2" r="2" fill="currentColor" />
            </svg>
            Aug 2021
            <div class="absolute -ml-2 h-px w-screen -translate-x-full bg-gray-900/10 sm:-ml-4 lg:static lg:-mr-6 lg:ml-8 lg:w-auto lg:flex-auto lg:translate-x-0" aria-hidden="true"></div>
          </time>
          <p class="mt-6 text-lg font-semibold leading-8 tracking-tight text-gray-900">Founded company</p>
          <p class="mt-1 text-base leading-7 text-gray-600">Nihil aut nam. Dignissimos a pariatur et quos omnis. Aspernatur asperiores et dolorem dolorem optio voluptate repudiandae.</p>
        </div>
        <div>
          <time datetime="2021-12" class="flex items-center text-sm font-semibold leading-6 text-indigo-600">
            <svg viewBox="0 0 4 4" class="mr-4 h-1 w-1 flex-none" aria-hidden="true">
              <circle cx="2" cy="2" r="2" fill="currentColor" />
            </svg>
            Dec 2021
            <div class="absolute -ml-2 h-px w-screen -translate-x-full bg-gray-900/10 sm:-ml-4 lg:static lg:-mr-6 lg:ml-8 lg:w-auto lg:flex-auto lg:translate-x-0" aria-hidden="true"></div>
          </time>
          <p class="mt-6 text-lg font-semibold leading-8 tracking-tight text-gray-900">Secured $65m in funding</p>
          <p class="mt-1 text-base leading-7 text-gray-600">Provident quia ut esse. Vero vel eos repudiandae aspernatur. Cumque minima impedit sapiente a architecto nihil.</p>
        </div>
        <div>
          <time datetime="2022-02" class="flex items-center text-sm font-semibold leading-6 text-indigo-600">
            <svg viewBox="0 0 4 4" class="mr-4 h-1 w-1 flex-none" aria-hidden="true">
              <circle cx="2" cy="2" r="2" fill="currentColor" />
            </svg>
            Feb 2022
            <div class="absolute -ml-2 h-px w-screen -translate-x-full bg-gray-900/10 sm:-ml-4 lg:static lg:-mr-6 lg:ml-8 lg:w-auto lg:flex-auto lg:translate-x-0" aria-hidden="true"></div>
          </time>
          <p class="mt-6 text-lg font-semibold leading-8 tracking-tight text-gray-900">Released beta</p>
          <p class="mt-1 text-base leading-7 text-gray-600">Sunt perspiciatis incidunt. Non necessitatibus aliquid. Consequatur ut officiis earum eum quia facilis. Hic deleniti dolorem quia et.</p>
        </div>
        <div>
          <time datetime="2022-12" class="flex items-center text-sm font-semibold leading-6 text-indigo-600">
            <svg viewBox="0 0 4 4" class="mr-4 h-1 w-1 flex-none" aria-hidden="true">
              <circle cx="2" cy="2" r="2" fill="currentColor" />
            </svg>
            Dec 2022
            <div class="absolute -ml-2 h-px w-screen -translate-x-full bg-gray-900/10 sm:-ml-4 lg:static lg:-mr-6 lg:ml-8 lg:w-auto lg:flex-auto lg:translate-x-0" aria-hidden="true"></div>
          </time>
          <p class="mt-6 text-lg font-semibold leading-8 tracking-tight text-gray-900">Global launch of product</p>
          <p class="mt-1 text-base leading-7 text-gray-600">Ut ipsa sint distinctio quod itaque nam qui. Possimus aut unde id architecto voluptatem hic aut pariatur velit.</p>
        </div>
      </div>
    </div>

    <!-- Logo cloud -->
    <div class="mx-auto mt-32 max-w-7xl sm:mt-40 sm:px-6 lg:px-8">
      <div class="relative isolate overflow-hidden bg-gray-900 px-6 py-24 text-center shadow-2xl sm:rounded-3xl sm:px-16">
        <h2 class="mx-auto max-w-2xl text-3xl font-bold tracking-tight text-white sm:text-4xl">Our customers love us</h2>
        <p class="mx-auto mt-6 max-w-xl text-lg leading-8 text-gray-300">Aliquip reprehenderit incididunt amet quis fugiat ut velit. Sit occaecat labore proident cillum in nisi adipisicing officia excepteur tempor deserunt.</p>
        <div class="mx-auto mt-20 grid max-w-lg grid-cols-4 items-center gap-x-8 gap-y-12 sm:max-w-xl sm:grid-cols-6 sm:gap-x-10 sm:gap-y-14 lg:max-w-4xl lg:grid-cols-5">
          <img class="col-span-2 max-h-12 w-full object-contain lg:col-span-1" src="https://tailwindui.com/img/logos/158x48/transistor-logo-white.svg" alt="Transistor" width="158" height="48">
          <img class="col-span-2 max-h-12 w-full object-contain lg:col-span-1" src="https://tailwindui.com/img/logos/158x48/reform-logo-white.svg" alt="Reform" width="158" height="48">
          <img class="col-span-2 max-h-12 w-full object-contain lg:col-span-1" src="https://tailwindui.com/img/logos/158x48/tuple-logo-white.svg" alt="Tuple" width="158" height="48">
          <img class="col-span-2 max-h-12 w-full object-contain sm:col-start-2 lg:col-span-1" src="https://tailwindui.com/img/logos/158x48/savvycal-logo-white.svg" alt="SavvyCal" width="158" height="48">
          <img class="col-span-2 col-start-2 max-h-12 w-full object-contain sm:col-start-auto lg:col-span-1" src="https://tailwindui.com/img/logos/158x48/statamic-logo-white.svg" alt="Statamic" width="158" height="48">
        </div>
        <div class="absolute -top-24 right-0 -z-10 transform-gpu blur-3xl" aria-hidden="true">
          <div class="aspect-[1404/767] w-[87.75rem] bg-gradient-to-r from-[#80caff] to-[#4f46e5] opacity-25" style="clip-path: polygon(73.6% 51.7%, 91.7% 11.8%, 100% 46.4%, 97.4% 82.2%, 92.5% 84.9%, 75.7% 64%, 55.3% 47.5%, 46.5% 49.4%, 45% 62.9%, 50.3% 87.2%, 21.3% 64.1%, 0.1% 100%, 5.4% 51.1%, 21.4% 63.9%, 58.9% 0.2%, 73.6% 51.7%)"></div>
        </div>
      </div>
    </div>

    <!-- Content section -->
    <div class="mt-32 overflow-hidden sm:mt-40">
      <div class="mx-auto max-w-7xl px-6 lg:flex lg:px-8">
        <div class="mx-auto grid max-w-2xl grid-cols-1 gap-x-12 gap-y-16 lg:mx-0 lg:min-w-full lg:max-w-none lg:flex-none lg:gap-y-8">
          <div class="lg:col-end-1 lg:w-full lg:max-w-lg lg:pb-8">
            <h2 class="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">Our people</h2>
            <p class="mt-6 text-xl leading-8 text-gray-600">Quasi est quaerat. Sit molestiae et. Provident ad dolorem occaecati eos iste. Soluta rerum quidem minus ut molestiae velit error quod. Excepturi quidem expedita molestias quas.</p>
            <p class="mt-6 text-base leading-7 text-gray-600">Anim aute id magna aliqua ad ad non deserunt sunt. Qui irure qui lorem cupidatat commodo. Elit sunt amet fugiat veniam occaecat fugiat. Quasi aperiam sit non sit neque reprehenderit.</p>
          </div>
          <div class="flex flex-wrap items-start justify-end gap-6 sm:gap-8 lg:contents">
            <div class="w-0 flex-auto lg:ml-auto lg:w-auto lg:flex-none lg:self-end">
              <img src="https://images.unsplash.com/photo-1670272502246-768d249768ca?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1152&q=80" alt="" class="aspect-[7/5] w-[37rem] max-w-none rounded-2xl bg-gray-50 object-cover">
            </div>
            <div class="contents lg:col-span-2 lg:col-end-2 lg:ml-auto lg:flex lg:w-[37rem] lg:items-start lg:justify-end lg:gap-x-8">
              <div class="order-first flex w-64 flex-none justify-end self-end lg:w-auto">
                <img src="https://images.unsplash.com/photo-1605656816944-971cd5c1407f?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=768&h=604&q=80" alt="" class="aspect-[4/3] w-[24rem] max-w-none flex-none rounded-2xl bg-gray-50 object-cover">
              </div>
              <div class="flex w-96 flex-auto justify-end lg:w-auto lg:flex-none">
                <img src="https://images.unsplash.com/photo-1568992687947-868a62a9f521?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1152&h=842&q=80" alt="" class="aspect-[7/5] w-[37rem] max-w-none flex-none rounded-2xl bg-gray-50 object-cover">
              </div>
              <div class="hidden sm:block sm:w-0 sm:flex-auto lg:w-auto lg:flex-none">
                <img src="https://images.unsplash.com/photo-1612872087720-bb876e2e67d1?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=768&h=604&q=80" alt="" class="aspect-[4/3] w-[24rem] max-w-none rounded-2xl bg-gray-50 object-cover">
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Content section -->
    <div class=" mx-auto mt-32 max-w-7xl px-6 sm:mt-40 lg:px-8">
      <div class="mx-auto flex max-w-2xl flex-col items-end justify-between gap-16 lg:mx-0 lg:max-w-none lg:flex-row">
        <div class="w-full lg:max-w-lg lg:flex-auto">
          <h2 class="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">We’re always looking for awesome people to join us</h2>
          <p class="mt-6 text-xl leading-8 text-gray-600">Diam nunc lacus lacus aliquam turpis enim. Eget hac velit est euismod lacus. Est non placerat nam arcu. Cras purus nibh cursus sit eu in id.</p>
          <img src="https://images.unsplash.com/photo-1606857521015-7f9fcf423740?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1344&h=1104&q=80" alt="" class="mt-16 aspect-[6/5] w-full rounded-2xl bg-gray-50 object-cover lg:aspect-auto lg:h-[34.5rem]">
        </div>
        <div class="w-full lg:max-w-xl lg:flex-auto">
          <h3 class="sr-only">Job openings</h3>
          <ul class="-my-8 divide-y divide-gray-100">
            <li class="py-8">
              <dl class="relative flex flex-wrap gap-x-3">
                <dt class="sr-only">Role</dt>
                <dd class="w-full flex-none text-lg font-semibold tracking-tight text-gray-900">
                  <a href="/">
                    Full-time designer
                    <span class="absolute inset-0" aria-hidden="true"></span>
                  </a>
                </dd>
                <dt class="sr-only">Description</dt>
                <dd class="mt-2 w-full flex-none text-base leading-7 text-gray-600">Quos sunt ad dolore ullam qui. Enim et quisquam dicta molestias. Corrupti quo voluptatum eligendi autem labore.</dd>
                <dt class="sr-only">Salary</dt>
                <dd class="mt-4 text-base font-semibold leading-7 text-gray-900">$75,000 USD</dd>
                <dt class="sr-only">Location</dt>
                <dd class="mt-4 flex items-center gap-x-3 text-base leading-7 text-gray-500">
                  <svg viewBox="0 0 2 2" class="h-0.5 w-0.5 flex-none fill-gray-300" aria-hidden="true">
                    <circle cx="1" cy="1" r="1" />
                  </svg>
                  San Francisco, CA
                </dd>
              </dl>
            </li>
            <li class="py-8">
              <dl class="relative flex flex-wrap gap-x-3">
                <dt class="sr-only">Role</dt>
                <dd class="w-full flex-none text-lg font-semibold tracking-tight text-gray-900">
                  <a href="/">
                    Laravel developer
                    <span class="absolute inset-0" aria-hidden="true"></span>
                  </a>
                </dd>
                <dt class="sr-only">Description</dt>
                <dd class="mt-2 w-full flex-none text-base leading-7 text-gray-600">Et veniam et officia dolorum rerum. Et voluptas consequatur magni sapiente amet voluptates dolorum. Ut porro aut eveniet.</dd>
                <dt class="sr-only">Salary</dt>
                <dd class="mt-4 text-base font-semibold leading-7 text-gray-900">$125,000 USD</dd>
                <dt class="sr-only">Location</dt>
                <dd class="mt-4 flex items-center gap-x-3 text-base leading-7 text-gray-500">
                  <svg viewBox="0 0 2 2" class="h-0.5 w-0.5 flex-none fill-gray-300" aria-hidden="true">
                    <circle cx="1" cy="1" r="1" />
                  </svg>
                  San Francisco, CA
                </dd>
              </dl>
            </li>
            <li class="py-8">
              <dl class="relative flex flex-wrap gap-x-3">
                <dt class="sr-only">Role</dt>
                <dd class="w-full flex-none text-lg font-semibold tracking-tight text-gray-900">
                  <a href="/">
                    React Native developer
                    <span class="absolute inset-0" aria-hidden="true"></span>
                  </a>
                </dd>
                <dt class="sr-only">Description</dt>
                <dd class="mt-2 w-full flex-none text-base leading-7 text-gray-600">Veniam ipsam nisi quas architecto eos non voluptatem in nemo. Est occaecati nihil omnis delectus illum est.</dd>
                <dt class="sr-only">Salary</dt>
                <dd class="mt-4 text-base font-semibold leading-7 text-gray-900">$105,000 USD</dd>
                <dt class="sr-only">Location</dt>
                <dd class="mt-4 flex items-center gap-x-3 text-base leading-7 text-gray-500">
                  <svg viewBox="0 0 2 2" class="h-0.5 w-0.5 flex-none fill-gray-300" aria-hidden="true">
                    <circle cx="1" cy="1" r="1" />
                  </svg>
                  San Francisco, CA
                </dd>
              </dl>
            </li>
          </ul>
          <div class="mt-8 flex border-t border-gray-100 pt-8">
            <a href="/" class="text-sm font-semibold leading-6 text-indigo-600 hover:text-indigo-500">View all openings <span aria-hidden="true">&rarr;</span></a>
          </div>
        </div>
      </div>
    </div>

  <!-- Contact Us Section -->
  <div id="contact" class="relative isolate px-6 py-24 sm:py-32 lg:px-8">
    <!-- <svg class="absolute inset-0 -z-10 h-full w-full stroke-gray-200 [mask-image:radial-gradient(100%_100%_at_top_right,white,transparent)]" aria-hidden="true">
      <defs>
        <pattern id="83fd4e5a-9d52-42fc-97b6-718e5d7ee527" width="200" height="200" x="50%" y="-64" patternUnits="userSpaceOnUse">
          <path d="M100 200V.5M.5 .5H200" fill="none" />
        </pattern>
      </defs>
      <svg x="50%" y="-64" class="overflow-visible fill-gray-50">
        <path d="M-100.5 0h201v201h-201Z M699.5 0h201v201h-201Z M499.5 400h201v201h-201Z M299.5 800h201v201h-201Z" stroke-width="0" />
      </svg>
      <rect width="100%" height="100%" stroke-width="0" fill="url(#83fd4e5a-9d52-42fc-97b6-718e5d7ee527)" />
    </svg> -->
    <div class="mx-auto max-w-xl lg:max-w-4xl">
      <h2 class="text-4xl font-bold tracking-tight text-gray-900">Looking for more information?</h2>
      <p class="mt-2 text-lg leading-8 text-gray-600">We are here to help in anyway. Simply fill out our form below and we will have someone contact you promptly.</p>
      <div class="mt-16 flex flex-col gap-16 sm:gap-y-20 lg:flex-row">
        <form action="#" method="POST" class="lg:flex-auto">
          <div class="grid grid-cols-1 gap-x-8 gap-y-6 sm:grid-cols-2">
            <div>
              <label for="first-name" class="block text-sm font-semibold leading-6 text-gray-900">Name</label>
              <div class="mt-2.5">
                <input type="text" name="first-name" id="first-name" autocomplete="given-name" class="block w-full rounded-md border-0 px-3.5 py-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6">
              </div>
            </div>
            <div>
              <label for="last-name" class="block text-sm font-semibold leading-6 text-gray-900">Email</label>
              <div class="mt-2.5">
                <input type="text" name="last-name" id="last-name" autocomplete="family-name" class="block w-full rounded-md border-0 px-3.5 py-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6">
              </div>
            </div>
            <div class="sm:col-span-2">
              <label for="message" class="block text-sm font-semibold leading-6 text-gray-900">Message</label>
              <div class="mt-2.5">
                <textarea id="message" name="message" rows="4" class="block w-full rounded-md border-0 px-3.5 py-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"></textarea>
              </div>
            </div>
          </div>
          <div class="mt-10">
            <button type="submit" class="block w-full rounded-md bg-nivaltaBlue px-3.5 py-2.5 text-center text-sm font-semibold text-white shadow-sm hover:bg-indigo-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">Let’s talk</button>
          </div>
          <p class="mt-4 text-sm leading-6 text-gray-500">By submitting this form, I agree to the <a href="/" class="font-semibold text-nivaltaBlue">privacy&nbsp;policy</a>.</p>
        </form>
        <div class="lg:mt-6 lg:w-80 lg:flex-none">
          <figure class="mt-2">
            <blockquote class="text-lg font-semibold leading-8 text-gray-900">
              <p>“I have been passionate about knowing more about my health through tracking data and seeing trends in my own lab work.  I hope to bring that same passion for healthcare data to individuals and doctors alike.”</p>
            </blockquote>
            <figcaption class="mt-10 flex gap-x-6">
              <img src="https://images.unsplash.com/photo-1550525811-e5869dd03032?ixlib=rb-=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=96&h=96&q=80" alt="" class="h-12 w-12 flex-none rounded-full bg-gray-50">
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
<footer id="waitlist" class="bg-gray-900" aria-labelledby="footer-heading">
  <h2 id="footer-heading" class="sr-only">Footer</h2>
  <div class="mx-auto max-w-7xl px-6 pb-8 pt-8 sm:pt-24 lg:px-8 lg:pt-8">
    <div class="xl:grid xl:grid-cols-3 xl:gap-8">
    </div>
    <div class="mt-16 border-t border-white/10 pt-8 sm:mt-20 lg:mt-24 lg:flex lg:items-center lg:justify-between">
      <div>
        <h3 class="text-sm font-semibold leading-6 text-white">Sign up today</h3>
        <p class="mt-2 text-sm leading-6 text-gray-300">Join our waitlist to be the first to hear about new features and updates.</p>
      </div>
      <form class="mt-6 sm:flex sm:max-w-md lg:mt-0">
        <label for="email-address" class="sr-only">Email address</label>
        <input type="email" name="email-address" id="email-address" autocomplete="email" required class="w-full min-w-0 appearance-none rounded-md border-0 bg-white/5 px-3 py-1.5 text-base text-white shadow-sm ring-1 ring-inset ring-white/10 placeholder:text-gray-500 focus:ring-2 focus:ring-inset focus:ring-indigo-500 sm:w-56 sm:text-sm sm:leading-6" placeholder="Enter your email">
        <div class="mt-4 sm:ml-4 sm:mt-0 sm:flex-shrink-0">
          <button type="submit" class="flex w-full items-center justify-center rounded-3xl bg-nivaltaBlue px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">Wait List</button>
        </div>
      </form>
    </div>
    <div class="mt-8 border-t border-white/10 pt-8 md:flex md:items-center md:justify-between">
      <p class="mt-8 text-xs leading-5 text-gray-400 md:order-1 md:mt-0">&copy; 2024 Nivalta, Inc. All rights reserved.</p>
    </div>
  </div>
</footer>


