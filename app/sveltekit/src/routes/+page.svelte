<script>

</script>

<header class="bg-white">
    <nav class="mx-auto flex items-center justify-between gap-x-6 p-6 lg:px-8" aria-label="Global">
        <div class="flex lg:flex-1">
        <a href="/" class="-m-1.5 p-1.5 text-nivaltaBlue font-bold text-3xl">Nivalta</a>
        </div>
        <div class="hidden lg:flex lg:gap-x-12">
        <a href="/" class="text-md font-semibold leading-6 text-gray-900">Home</a>
        <a href="/" class="text-md font-semibold leading-6 text-gray-900">Features</a>
        <a href="/" class="text-md font-semibold leading-6 text-gray-900">About Us</a>
        <a href="/" class="text-md font-semibold leading-6 text-gray-900">Contact</a>
        </div>
        <div class="flex flex-1 items-center justify-end gap-x-6">
        <a href="/" class="rounded-3xl bg-nivaltaBlue px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">Wait List</a>
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
<!--             <div class="py-6">
                <a href="/" class="-mx-3 block rounded-lg px-3 py-2.5 text-base font-semibold leading-7 text-gray-900 hover:bg-gray-50">Wait List</a>
            </div> -->
            </div>
        </div>
        </div>
    </div>
</header>

<main class="isolate bg-slate-100">
        <!-- Hero Section -->
        <div class="relative overflow-hidden pb-32 pt-16">
            <div aria-hidden="true" class="absolute inset-x-0 top-0 h-48 from-gray-100"></div>
            <div class="relative">
              <div class="lg:mx-auto lg:grid lg:max-w-7xl lg:grid-flow-col-dense lg:grid-cols-2 lg:gap-24 lg:px-8">
                <div class="mx-auto max-w-xl px-6 lg:mx-0 lg:max-w-none lg:px-0 lg:py-16">
                  <div>
                    <div>
                      <span class="flex h-12 w-12 items-center justify-center rounded-md bg-gradient-to-r from-purple-600 to-indigo-600">
                        <svg class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" aria-hidden="true">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 13.5h3.86a2.25 2.25 0 012.012 1.244l.256.512a2.25 2.25 0 002.013 1.244h3.218a2.25 2.25 0 002.013-1.244l.256-.512a2.25 2.25 0 012.013-1.244h3.859m-19.5.338V18a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18v-4.162c0-.224-.034-.447-.1-.661L19.24 5.338a2.25 2.25 0 00-2.15-1.588H6.911a2.25 2.25 0 00-2.15 1.588L2.35 13.177a2.25 2.25 0 00-.1.661z" />
                        </svg>
                      </span>
                    </div>
                    <div class="mt-6">
                      <h2 class="text-3xl font-bold tracking-tight text-gray-900">Transform your health data into personalized insights</h2>
                      <p class="mt-4 text-lg text-gray-500">Seamlessly combine your health records, symptoms, habits, and history to unlock personalized wellness strategies.</p>
                      <div class="mt-6">
                        <a href="/" class="inline-flex rounded-3xl border border-transparent bg-nivaltaBlue  px-4 py-2 text-base font-medium text-white shadow-sm hover:from-purple-700 hover:bg-indigo-600">Wait List</a>
                      </div>
                    </div>
                  </div>
                  <div class="mt-8 border-t border-gray-200 pt-6">
                    <blockquote>
                      <div>
                        <p class="text-base text-gray-500">&ldquo;Cras velit quis eros eget rhoncus lacus ultrices sed diam. Sit orci risus aenean curabitur donec aliquet. Mi venenatis in euismod ut.&rdquo;</p>
                      </div>
                      <footer class="mt-3">
                        <div class="flex items-center space-x-3">
                          <div class="flex-shrink-0">
                            <img class="h-6 w-6 rounded-full" src="https://images.unsplash.com/photo-1509783236416-c9ad59bae472?ixlib=rb-=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=8&w=1024&h=1024&q=80" alt="">
                          </div>
                          <div class="text-base font-medium text-gray-700">Marcia Hill, Digital Marketing Manager</div>
                        </div>
                      </footer>
                    </blockquote>
                  </div>
                </div>
                <div class="mt-12 sm:mt-16 lg:mt-0">
                  <div class="-mr-48 pl-6 md:-mr-16 lg:relative lg:m-0 lg:h-full lg:px-0">
                    <img class="w-full rounded-xl shadow-xl ring-1 ring-black ring-opacity-5 lg:absolute lg:left-0 lg:h-full lg:w-auto lg:max-w-none" src="https://tailwindui.com/img/component-images/inbox-app-screenshot-1.jpg" alt="Inbox user interface">
                  </div>
                </div>
              </div>
            </div>
            <div class="mt-24">
              <div class="lg:mx-auto lg:grid lg:max-w-7xl lg:grid-flow-col-dense lg:grid-cols-2 lg:gap-24 lg:px-8">
                <div class="mx-auto max-w-xl px-6 lg:col-start-2 lg:mx-0 lg:max-w-none lg:px-0 lg:py-32">
                  <div>
                    <div>
                      <span class="flex h-12 w-12 items-center justify-center rounded-md bg-gradient-to-r from-purple-600 to-indigo-600">
                        <svg class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" aria-hidden="true">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456zM16.894 20.567L16.5 21.75l-.394-1.183a2.25 2.25 0 00-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 001.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 001.423 1.423l1.183.394-1.183.394a2.25 2.25 0 00-1.423 1.423z" />
                        </svg>
                      </span>
                    </div>
                    <div class="mt-6">
                      <h2 class="text-3xl font-bold tracking-tight text-gray-900">Better understand your customers</h2>
                      <p class="mt-4 text-lg text-gray-500">Semper curabitur ullamcorper posuere nunc sed. Ornare iaculis bibendum malesuada faucibus lacinia porttitor. Pulvinar laoreet sagittis viverra duis. In venenatis sem arcu pretium pharetra at. Lectus viverra dui tellus ornare pharetra.</p>
                      <div class="mt-6">
                        <a href="/" class="inline-flex rounded-md border border-transparent bg-nivaltaBlue  bg-origin-border px-4 py-2 text-base font-medium text-white shadow-sm hover:from-purple-700 hover:bg-indigo-600">Get started</a>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="mt-12 sm:mt-16 lg:col-start-1 lg:mt-0">
                  <div class="-ml-48 pr-6 md:-ml-16 lg:relative lg:m-0 lg:h-full lg:px-0">
                    <img class="w-full rounded-xl shadow-xl ring-1 ring-black ring-opacity-5 lg:absolute lg:right-0 lg:h-full lg:w-auto lg:max-w-none" src="https://tailwindui.com/img/component-images/inbox-app-screenshot-2.jpg" alt="Customer profile user interface">
                  </div>
                </div>
              </div>
            </div>
          </div>
        <!-- About Us Section -->
        <div class="relative mx-auto mt-0 max-w-7xl px-6 sm:mt-0 lg:px-8 xl:mt-4">
            <div class="mx-auto my-auto max-w-2xl lg:mx-0 lg:max-w-none">
            <h2 class="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">Our mission</h2>
            <div class="mt-6 flex flex-col gap-x-8 gap-y-20 lg:flex-row">
                <div class="lg:w-full lg:max-w-2xl lg:flex-auto">
                <p class="text-xl leading-8 text-white">Aliquet nec orci mattis amet quisque ullamcorper neque, nibh sem. At arcu, sit dui mi, nibh dui, diam eget aliquam. Quisque id at vitae feugiat egestas ac. Diam nulla orci at in viverra scelerisque eget. Eleifend egestas fringilla sapien.</p>
                <div class="mt-10 max-w-xl text-base leading-7 text-white">
                    <p>Faucibus commodo massa rhoncus, volutpat. Dignissim sed eget risus enim. Mattis mauris semper sed amet vitae sed turpis id. Id dolor praesent donec est. Odio penatibus risus viverra tellus varius sit neque erat velit. Faucibus commodo massa rhoncus, volutpat. Dignissim sed eget risus enim. Mattis mauris semper sed amet vitae sed turpis id.</p>
                    <p class="mt-10">Et vitae blandit facilisi magna lacus commodo. Vitae sapien duis odio id et. Id blandit molestie auctor fermentum dignissim. Lacus diam tincidunt ac cursus in vel. Mauris varius vulputate et ultrices hac adipiscing egestas. Iaculis convallis ac tempor et ut. Ac lorem vel integer orci.</p>
                </div>
                </div>
                <div class="lg:flex lg:flex-auto lg:justify-center">
                <dl class="w-64 space-y-8 xl:w-80">
                    <div class="flex flex-col-reverse gap-y-4">
                    <dt class="text-base leading-7 text-gray-600">Transactions every 24 hours</dt>
                    <dd class="text-5xl font-semibold tracking-tight text-gray-900">44 million</dd>
                    </div>
                    <div class="flex flex-col-reverse gap-y-4">
                    <dt class="text-base leading-7 text-gray-600">Assets under holding</dt>
                    <dd class="text-5xl font-semibold tracking-tight text-gray-900">$119 trillion</dd>
                    </div>
                    <div class="flex flex-col-reverse gap-y-4">
                    <dt class="text-base leading-7 text-gray-600">New users annually</dt>
                    <dd class="text-5xl font-semibold tracking-tight text-gray-900">46,000</dd>
                    </div>
                </dl>
                </div>
            </div>
            </div>
        </div>
        
        <!-- Image section -->
        <div class="mt-32 sm:mt-40 xl:mx-auto xl:max-w-7xl xl:px-8">
            <img src="https://images.unsplash.com/photo-1529156069898-49953e39b3ac?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2832&q=80" alt="" class="aspect-[5/2] w-full object-cover xl:rounded-3xl">
        </div>
        
        <!-- Values section -->
        <div class="mx-auto mt-32 max-w-7xl px-6 sm:mt-40 lg:px-8">
            <div class="mx-auto max-w-2xl lg:mx-0">
            <h2 class="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">Our values</h2>
            <p class="mt-6 text-lg leading-8 text-gray-600">Lorem ipsum dolor sit amet consect adipisicing elit. Possimus magnam voluptatum cupiditate veritatis in accusamus quisquam.</p>
            </div>
            <dl class="mx-auto mt-16 grid max-w-2xl grid-cols-1 gap-x-8 gap-y-16 text-base leading-7 sm:grid-cols-2 lg:mx-0 lg:max-w-none lg:grid-cols-3">
            <div>
                <dt class="font-semibold text-gray-900">Be world-class</dt>
                <dd class="mt-1 text-gray-600">Aut illo quae. Ut et harum ea animi natus. Culpa maiores et sed sint et magnam exercitationem quia. Ullam voluptas nihil vitae dicta molestiae et. Aliquid velit porro vero.</dd>
            </div>
            <div>
                <dt class="font-semibold text-gray-900">Share everything you know</dt>
                <dd class="mt-1 text-gray-600">Mollitia delectus a omnis. Quae velit aliquid. Qui nulla maxime adipisci illo id molestiae. Cumque cum ut minus rerum architecto magnam consequatur. Quia quaerat minima.</dd>
            </div>
            <div>
                <dt class="font-semibold text-gray-900">Always learning</dt>
                <dd class="mt-1 text-gray-600">Aut repellendus et officiis dolor possimus. Deserunt velit quasi sunt fuga error labore quia ipsum. Commodi autem voluptatem nam. Quos voluptatem totam.</dd>
            </div>
            <div>
                <dt class="font-semibold text-gray-900">Be supportive</dt>
                <dd class="mt-1 text-gray-600">Magnam provident veritatis odit. Vitae eligendi repellat non. Eum fugit impedit veritatis ducimus. Non qui aspernatur laudantium modi. Praesentium rerum error deserunt harum.</dd>
            </div>
            <div>
                <dt class="font-semibold text-gray-900">Take responsibility</dt>
                <dd class="mt-1 text-gray-600">Sit minus expedita quam in ullam molestiae dignissimos in harum. Tenetur dolorem iure. Non nesciunt dolorem veniam necessitatibus laboriosam voluptas perspiciatis error.</dd>
            </div>
            <div>
                <dt class="font-semibold text-gray-900">Enjoy downtime</dt>
                <dd class="mt-1 text-gray-600">Ipsa in earum deserunt aut. Quos minus aut animi et soluta. Ipsum dicta ut quia eius. Possimus reprehenderit iste aspernatur ut est velit consequatur distinctio.</dd>
            </div>
            </dl>
        </div>
</main>

