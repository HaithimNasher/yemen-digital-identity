(() => {
  const STORAGE_LANG='ydii-language';
  const STORAGE_THEME='ydii-theme';

  const fallbackNav=[
    ['index.html','home','الرئيسية','Home'],
    ['domain-search.html','search','بحث النطاقات','Domain Search'],
    ['national-dashboard.html','dashboard','اللوحة الوطنية','National Dashboard'],
    ['directory.html','directory','الدليل الوطني','National Directory'],
    ['observatory.html','observatory','المرصد التقني','Observatory'],
    ['policy-center.html','policies','مركز السياسات','Policy Center'],
    ['namespace-model.html','namespace','نموذج النطاقات','Namespace Model'],
    ['registry-model.html','registry','نموذج السجل','Registry Model'],
    ['eligibility.html','eligibility','الأهلية','Eligibility'],
    ['gcc-benchmark.html','gcc','مقارنة الخليج','GCC Benchmark']
  ].map(([href,key,ar,en])=>({href,key,ar,en}));

  const labels={
    ar:{
      tagline:'مبادرة الهوية الرقمية اليمنية',
      language:'English',
      theme:'المظهر',
      skip:'تخطي إلى المحتوى',
      footer:'YDII Professional v2 — مشروع بحثي وهندسي مفتوح المصدر، وليس سجل .ye الرسمي.'
    },
    en:{
      tagline:'Yemen Digital Identity Initiative',
      language:'العربية',
      theme:'Theme',
      skip:'Skip to content',
      footer:'YDII Professional v2 — an open-source research and engineering project, not the official .ye registry.'
    }
  };

  let lang=localStorage.getItem(STORAGE_LANG) || 'ar';
  let theme=localStorage.getItem(STORAGE_THEME) ||
    (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');

  function currentFile(){
    return location.pathname.split('/').pop() || 'index.html';
  }

  function applyDocumentState(){
    document.documentElement.lang=lang;
    document.documentElement.dir=lang==='ar' ? 'rtl' : 'ltr';
    document.documentElement.dataset.theme=theme;
  }

  async function getNav(){
    try{
      const r=await fetch('data/navigation.json',{cache:'no-store'});
      if(!r.ok) throw new Error('navigation fetch failed');
      const d=await r.json();
      return d.items || fallbackNav;
    }catch(_){
      return fallbackNav;
    }
  }

  function ensureMainId(){
    const main=document.querySelector('main');
    if(main && !main.id) main.id='main-content';
  }

  async function renderShell(){
    applyDocumentState();
    ensureMainId();

    const nav=await getNav();
    document.querySelectorAll('.ydii-shell,.ydii-footer,.ydii-skip,.ydii-statusbar').forEach(x=>x.remove());

    const skip=document.createElement('a');
    skip.className='ydii-skip';
    skip.href='#main-content';
    skip.textContent=labels[lang].skip;
    document.body.prepend(skip);

    const header=document.createElement('header');
    header.className='ydii-shell';
    header.innerHTML=`
      <div class="ydii-shell-inner">
        <a class="ydii-brand" href="index.html" aria-label="YDII">
          <span class="ydii-mark">YE</span>
          <span class="ydii-brand-text">
            <b>YDII</b>
            <small>${labels[lang].tagline}</small>
          </span>
        </a>
        <nav class="ydii-nav" aria-label="${lang==='ar'?'التنقل الرئيسي':'Primary navigation'}">
          ${nav.map(x=>`
            <a href="${x.href}" ${x.href===currentFile()?'aria-current="page"':''}>
              ${lang==='ar'?x.ar:x.en}
            </a>
          `).join('')}
        </nav>
        <div class="ydii-actions">
          <button class="ydii-action" id="ydii-lang" type="button">${labels[lang].language}</button>
          <button class="ydii-action" id="ydii-theme" type="button" aria-label="${labels[lang].theme}">
            ${theme==='dark'?'☀':'◐'}
          </button>
        </div>
      </div>
    `;
    document.body.insertBefore(header,document.body.children[1] || null);

    const status=document.createElement('div');
    status.className='ydii-statusbar';
    status.innerHTML=`
      <span class="ydii-chip">YDII Professional v2</span>
      <span class="ydii-chip">Research / Engineering</span>
      <span class="ydii-chip">Not official .ye registry</span>
    `;
    header.after(status);

    const footer=document.createElement('footer');
    footer.className='ydii-footer';
    footer.textContent=labels[lang].footer;
    document.body.appendChild(footer);

    document.getElementById('ydii-lang').addEventListener('click',()=>{
      lang=lang==='ar'?'en':'ar';
      localStorage.setItem(STORAGE_LANG,lang);
      renderShell();
    });

    document.getElementById('ydii-theme').addEventListener('click',()=>{
      theme=theme==='dark'?'light':'dark';
      localStorage.setItem(STORAGE_THEME,theme);
      applyDocumentState();
      document.getElementById('ydii-theme').textContent=theme==='dark'?'☀':'◐';
    });
  }

  if(document.readyState==='loading'){
    document.addEventListener('DOMContentLoaded',renderShell);
  }else{
    renderShell();
  }
})();
