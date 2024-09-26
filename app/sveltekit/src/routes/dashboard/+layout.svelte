<script>
	import '../../app.css';
  import { afterNavigate, goto } from '$app/navigation';
  /** @type {import('./$types').LayoutData} */
	export let data;

  afterNavigate(() => {
    const session = data.sessionData;
    console.log('Login Status:', session);
    if (!session) {
      goto('/login');
    }
  });

  import { logout } from '$lib/session_data';

</script>


<div class="DashboardLeftNav w-[1536px] h-[1042px] relative bg-white rounded-[10px]">
  <img class="Nivalta13 w-[173px] h-[173px] left-[26px] top-[-24px] absolute" src="/images/nivalta-logo.svg" alt="Nivalta Company Logo" />
  
  <div class="Frame10 w-[216px] h-[337px] left-[41px] top-[149px] absolute flex-col justify-start items-start gap-2.5 inline-flex">
    <div class="Frame11 w-[146px] py-2 justify-start items-center gap-2.5 inline-flex">
      <div class="Overview grow shrink basis-0 text-[#3f3f3f] text-base font-semibold font-['Poppins'] uppercase">OVERVIEW</div>
    </div>
    <div class="Frame17 flex-col justify-center items-center gap-2 flex">
      <div class="Btn w-[146px] py-2 rounded-[40px] justify-start items-center gap-3 inline-flex">
        <div class="VuesaxLinearDirectInbox w-4 h-4 justify-center items-center flex">
          <div class="DirectInbox w-4 h-4 relative">
			<img src="/images/vuesax-linear-direct-inbox.svg" alt="An Inbox Symbol">
          </div>
        </div>
        <div class="Dashboard grow shrink basis-0 text-[#202020] text-base font-normal font-['Poppins']">
			<a href="/dashboard">Dashboard</a>
		</div>
      </div>
      <div class="Btn w-[146px] py-2 rounded-[40px] justify-start items-center gap-3 inline-flex">
        <div class="VuesaxLinearFolderOpen w-4 h-4 justify-center items-center flex">
          <div class="FolderOpen w-4 h-4 relative">
			<a href="/dashboard/symptoms">
				<img src="/images/vuesax-linear-open-folder.svg" alt="An Open Folder Icon">
			</a>
          </div>
        </div>
        <div class="Dashboard grow shrink basis-0 text-[#202020] text-base font-medium font-['Poppins']">
			<a href="/dashboard/symptoms">Symptom Log</a></div>
      </div>
      <div class="Btn w-[146px] py-2 rounded-[40px] justify-start items-center gap-3 inline-flex">
        <div class="VuesaxLinearTaskSquare w-4 h-4 justify-center items-center flex">
          <div class="TaskSquare w-4 h-4 relative">
			<a href="/dashboard/lab-results">
				<img src="/images/vuesax-linear-task-square.svg" alt="A Task List Icon">
			</a>
		  </div>
        </div>
        <div class="Dashboard grow shrink basis-0 text-[#202020] text-base font-medium font-['Poppins']">
			<a href="/dashboard/lab-results">Lab Results</a>
		</div>
      </div>
      <div class="Btn w-[146px] py-2 rounded-[40px] justify-start items-center gap-3 inline-flex">
        <div class="VuesaxLinearPeople w-4 h-4 justify-center items-center flex">
          <div class="People w-4 h-4 relative">
				<img src="/images/vuesax-linear-people.svg" alt="A group of 3 people icons">
            <div class="Group w-[4.43px] h-[8.35px] left-[10.22px] top-[1.33px] absolute">
            </div>
            <div class="Group w-[4.42px] h-[8.35px] left-[1.34px] top-[1.33px] absolute">
            </div>
            <div class="Group w-[5.29px] h-[8.35px] left-[5.36px] top-[6.31px] absolute">
            </div>
          </div>
        </div>
        <div class="Dashboard grow shrink basis-0 text-[#202020] text-base font-medium font-['Poppins']">Family History</div>
      </div>
      <div class="Btn w-[146px] py-2 rounded-[40px] justify-start items-center gap-3 inline-flex">
        <div class="VuesaxLinearPeople w-4 h-4 justify-center items-center flex">
          <div class="People w-4 h-4 relative">
			<img src="/images/vuesax-linear-people.svg" alt="A group of 3 people icons">
            <div class="Group w-[4.43px] h-[8.35px] left-[10.22px] top-[1.33px] absolute">
            </div>
            <div class="Group w-[4.42px] h-[8.35px] left-[1.34px] top-[1.33px] absolute">
            </div>
            <div class="Group w-[5.29px] h-[8.35px] left-[5.36px] top-[6.31px] absolute">
            </div>
          </div>
        </div>
        <div class="Dashboard grow shrink basis-0 text-[#202020] text-base font-medium font-['Poppins']">Insights</div>
      </div>
    </div>
  </div>
  <div class="Frame12 h-[140px] left-[40px] top-[880px] absolute flex-col justify-start items-start gap-2.5 inline-flex">
    <div class="Frame11 self-stretch py-2 justify-start items-center gap-2.5 inline-flex">
      <div class="Settings grow shrink basis-0 text-[#3f3f3f] text-base font-semibold font-['Poppins'] uppercase">SETTINGS</div>
    </div>
    <div class="Btn self-stretch py-2 rounded-[40px] justify-start items-center gap-3 inline-flex">
      <div class="VuesaxLinearSetting2 w-4 h-4 justify-center items-center flex">
        <div class="Setting2 w-4 h-4 relative">
			<img src="/images/vuesax-linear-setting2.svg" alt="A settings gear">
        </div>
      </div>
      <div class="Dashboard grow shrink basis-0 text-[#202020] text-base font-bold font-['Poppins']">Settings</div>
    </div>
    <div class="Btn self-stretch py-2 rounded-[40px] justify-start items-center gap-3 inline-flex">
      <div class="VuesaxLinearLogout w-4 h-4 justify-center items-center flex">
        <div class="Logout w-4 h-4 relative">
			<img src="/images/vuesax-linear-logout.svg" alt="A logout icon">
		</div>
      </div>
      <div class="Dashboard grow shrink basis-0 text-[#f13e3e] text-base font-medium font-['Poppins']">
		<a href="/login" on:click={logout}>Logout</a>
	</div>
    </div>
  </div>
  <slot />
</div>
