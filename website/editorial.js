const app = document.querySelector('#app');
const nav = document.querySelector('.nav');
const toggle = document.querySelector('.menu-toggle');
if(new URLSearchParams(location.search).get('embed') === 'profile') {
  document.documentElement.classList.add('profile-embed');
}
const icon = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>';
const contactLink = (title,detail,href) => `<a class="contact-link" href="${href}" ${href.startsWith('https:') ? 'target="_blank" rel="noreferrer"' : ''}><span class="contact-label"><strong>${title}</strong><small>${detail}</small></span><span class="contact-arrow" aria-hidden="true">${icon}</span></a>`;
const item = (number,title,copy) => `<article class="detail-item"><span class="number">${number}</span><h2>${title}</h2><p>${copy}</p></article>`;
const pages = {
  home: () => `<section class="page home" aria-labelledby="home-title"><h1 id="home-title" class="screen-reader">Usama Faheem, Frontend and MERN Stack Developer</h1><div class="home-role">+ MERN Stack</div><a class="view-work" href="https://usamafaheem.com/" target="_blank" rel="noreferrer" aria-label="View my work"></a><aside class="availability"><small>Available for</small><strong>Frontend &amp; MERN<br>projects</strong></aside><div class="mobile-copy"><h1>Usama<br><span>Faheem</span></h1><p>Frontend Developer + MERN Stack</p><a class="button" href="https://usamafaheem.com/" target="_blank" rel="noreferrer">View work</a></div></section>`,
  about: () => `<section class="page inside about"><div class="inside-copy"><span class="eyebrow">01 / About me</span><h1>Design.<br>Code.<br><em>Create.</em></h1><p>I'm Usama Faheem, a frontend focused MERN stack developer based in Lahore.</p><p>I build responsive websites with React and Next.js, connect APIs and databases, and add motion that makes interfaces feel alive.</p><a class="button" href="#contact">Let's connect</a></div><aside class="detail-panel">${item('FRONTEND','React & Next.js','Reusable components, responsive layouts and smooth interactions.')}${item('FULL STACK','MERN','Node.js, Express, MongoDB and REST APIs.')}${item('EXPERIENCE','Real client work','SoftCr8ors, UK service websites, Shadab Rice and Reeba.')}</aside></section>`,
  services: () => `<section class="page inside services"><div class="inside-copy"><span class="eyebrow">02 / Services</span><h1>Built to<br><em>stand out.</em></h1><p>From a company website to a working web app. Thoughtful design, clear interactions and solid development.</p><a class="button" href="#contact">Discuss a project</a></div><aside class="detail-panel">${item('01','Website development','Responsive business websites and portfolios with React and Next.js.')}${item('02','Motion & 3D','Framer Motion, Three.js and React Three Fiber.')}${item('03','MERN applications','APIs, databases, admin panels and AI integration.')}${item('04','Quality & performance','SEO, accessibility, browser compatibility and loading speed.')}</aside></section>`,
  contact: () => `<section class="page inside contact"><div class="inside-copy"><span class="eyebrow">03 / Contact</span><h1>Let's build<br><em>something.</em></h1><p>Open to frontend developer roles, MERN stack internships and freelance projects.</p><p>Lahore, Pakistan</p><a class="button" href="mailto:developer@usamafaheem.com">Email me</a></div><aside class="detail-panel" aria-label="Contact links">${contactLink('Email','developer@usamafaheem.com','mailto:developer@usamafaheem.com')}${contactLink('Portfolio','usamafaheem.com','https://usamafaheem.com/')}${contactLink('LinkedIn','in/usama-faheem','https://www.linkedin.com/in/usama-faheem/')}${contactLink('GitHub','usamafaheem-dev','https://github.com/usamafaheem-dev')}</aside></section>`
};
function route() {
  const key = location.hash.slice(1) || 'home';
  const page = pages[key] ? key : 'home';
  app.innerHTML = pages[page]();
  if(new URLSearchParams(location.search).get('embed') === 'profile') {
    app.querySelectorAll('.view-work,.mobile-copy .button').forEach(link=>{
      link.href='../PREVIEW.html#selected-work';
      link.target='_top';
    });
  }
  document.title = `${page.charAt(0).toUpperCase() + page.slice(1)} | Usama Faheem`;
  document.querySelectorAll('[data-route]').forEach(link => {
    const current = link.dataset.route === page;
    link.classList.toggle('active',current);
    if (current) link.setAttribute('aria-current','page'); else link.removeAttribute('aria-current');
  });
  nav.classList.remove('open');
  toggle.setAttribute('aria-expanded','false');
}
toggle.addEventListener('click',() => { const open = nav.classList.toggle('open'); toggle.setAttribute('aria-expanded',String(open)); });
document.addEventListener('keydown',event => { if(event.key === 'Escape') { nav.classList.remove('open'); toggle.setAttribute('aria-expanded','false'); toggle.focus(); } });
window.addEventListener('hashchange',route);
route();
