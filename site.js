(() => {
  'use strict';
  const toggle = document.querySelector('.language-toggle');
  const languageName = toggle.querySelector('.language-name');
  const storageKey = 'pengbo-li-language';
  const params = new URLSearchParams(window.location.search);
  const requestedLanguage = params.get('lang');
  let savedLanguage;
  try { savedLanguage = localStorage.getItem(storageKey); } catch { /* Private browsing still works. */ }
  let language = (requestedLanguage === 'zh' || requestedLanguage === 'en')
    ? requestedLanguage : (savedLanguage === 'zh' ? 'zh' : 'en');

  function setLanguage(nextLanguage, remember = false) {
    language = nextLanguage;
    document.documentElement.lang = language === 'zh' ? 'zh-CN' : 'en';
    document.querySelectorAll('[data-en][data-zh]').forEach(element => {
      element.textContent = element.getAttribute(`data-${language}`);
    });
    document.querySelectorAll('[data-alt-en]').forEach(element => {
      element.alt = element.getAttribute(`data-alt-${language}`);
    });
    document.querySelectorAll('[data-label-en]').forEach(element => {
      element.setAttribute('aria-label', element.getAttribute(`data-label-${language}`));
    });
    document.querySelector('.name-secondary').lang = language === 'zh' ? 'en' : 'zh-CN';
    languageName.textContent = language === 'en' ? '中文' : 'English';
    toggle.setAttribute('aria-label', language === 'en' ? '切换为中文' : 'Switch to English');
    toggle.title = toggle.getAttribute('aria-label');
    document.title = language === 'zh' ? '李鹏博 · 机器学习系统' : 'Pengbo Li · Machine Learning Systems';
    const description = language === 'zh'
      ? '李鹏博，香港科技大学计算机系博士生。研究机器学习系统、大语言模型强化学习与高效训练基础设施。'
      : 'Pengbo Li (李鹏博), Ph.D. student at HKUST. Research in machine learning systems, LLM reinforcement learning, and efficient training infrastructure.';
    document.querySelector('meta[name="description"]').content = description;
    document.querySelector('meta[property="og:title"]').content = document.title;
    document.querySelector('meta[property="og:description"]').content = description;
    if (remember) {
      try { localStorage.setItem(storageKey, language); } catch { /* Preference persistence is optional. */ }
      try {
        const url = new URL(window.location.href);
        url.searchParams.set('lang', language);
        history.replaceState(null, '', url);
      } catch { /* Local file previews may restrict history updates. */ }
    }
  }

  setLanguage(language);
  toggle.hidden = false;
  toggle.addEventListener('click', () => setLanguage(language === 'en' ? 'zh' : 'en', true));

  const navigation = [...document.querySelectorAll('nav a')];
  const sections = navigation.map(link => document.querySelector(link.getAttribute('href')));
  function updateNavigation() {
    const cutoff = document.querySelector('.site-header').getBoundingClientRect().height + 110;
    let current = sections[0];
    for (const section of sections) {
      if (section.getBoundingClientRect().top <= cutoff) current = section;
    }
    if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 4) {
      current = sections[sections.length - 1];
    }
    navigation.forEach(link => {
      const active = link.getAttribute('href') === `#${current.id}`;
      link.classList.toggle('active', active);
      if (active) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
  }
  let framePending = false;
  window.addEventListener('scroll', () => {
    if (framePending) return;
    framePending = true;
    requestAnimationFrame(() => { updateNavigation(); framePending = false; });
  }, { passive: true });
  window.addEventListener('resize', updateNavigation);
  updateNavigation();
})();
