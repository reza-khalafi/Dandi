/**
 * Dandi Magazine - Core Interactive Controller
 * Handles Theme Switching, Hero Parallax, Live Search & Infinite Scroll
 */

document.addEventListener('DOMContentLoaded', () => {
  initThemeManager();
  initParallaxEffects();
  initArticleFeedManager();
  initCommentAjaxHandler();
});

/* ----------------------------------------------------
   1. Multi-Theme Switching Manager
   ---------------------------------------------------- */
function initThemeManager() {
  const root = document.documentElement;
  const storageKey = 'dandi_theme_preference';
  const savedTheme = localStorage.getItem(storageKey) || 'light';

  setTheme(savedTheme);

  // Dropdown toggler
  const themeBtn = document.getElementById('theme-menu-button');
  const themeDropdown = document.getElementById('theme-dropdown-menu');

  if (themeBtn && themeDropdown) {
    themeBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      themeDropdown.classList.toggle('hidden');
    });

    document.addEventListener('click', () => {
      if (!themeDropdown.classList.contains('hidden')) {
        themeDropdown.classList.add('hidden');
      }
    });

    // Theme selector buttons
    document.querySelectorAll('[data-set-theme]').forEach((btn) => {
      btn.addEventListener('click', (e) => {
        const selectedTheme = btn.getAttribute('data-set-theme');
        setTheme(selectedTheme);
        themeDropdown.classList.add('hidden');
      });
    });
  }

  function setTheme(themeName) {
    root.setAttribute('data-theme', themeName);
    localStorage.setItem(storageKey, themeName);

    // Update active checkmarks or highlights in dropdown
    document.querySelectorAll('[data-set-theme]').forEach((btn) => {
      const isCurrent = btn.getAttribute('data-set-theme') === themeName;
      const indicator = btn.querySelector('.theme-active-indicator');
      if (indicator) {
        indicator.classList.toggle('opacity-100', isCurrent);
        indicator.classList.toggle('opacity-0', !isCurrent);
      }
    });
  }
}

/* ----------------------------------------------------
   2. Parallax Motion & Floating Elements
   ---------------------------------------------------- */
function initParallaxEffects() {
  const heroSection = document.getElementById('hero-section');
  const parallaxOrbs = document.querySelectorAll('.parallax-orb');
  const dandelionSeeds = document.querySelectorAll('.floating-seed');

  // Mouse move parallax on Hero
  if (heroSection && window.innerWidth > 768) {
    heroSection.addEventListener('mousemove', (e) => {
      const rect = heroSection.getBoundingClientRect();
      const xRatio = (e.clientX - rect.left) / rect.width - 0.5;
      const yRatio = (e.clientY - rect.top) / rect.height - 0.5;

      parallaxOrbs.forEach((orb) => {
        const factor = parseFloat(orb.getAttribute('data-parallax-factor') || '20');
        orb.style.transform = `translate3d(${xRatio * factor}px, ${yRatio * factor}px, 0)`;
      });

      dandelionSeeds.forEach((seed) => {
        const factor = parseFloat(seed.getAttribute('data-parallax-factor') || '35');
        seed.style.transform = `translate3d(${xRatio * factor}px, ${yRatio * factor}px, 0) rotate(${xRatio * 15}deg)`;
      });
    });
  }

  // Smooth Scroll parallax
  window.addEventListener('scroll', () => {
    const scrollY = window.pageYOffset || document.documentElement.scrollTop;
    if (scrollY < 800) {
      parallaxOrbs.forEach((orb) => {
        const factor = parseFloat(orb.getAttribute('data-scroll-factor') || '0.1');
        orb.style.marginTop = `${scrollY * factor}px`;
      });
    }
  }, { passive: true });
}

/* ----------------------------------------------------
   3. Incremental Article Loading & Live Search
   ---------------------------------------------------- */
function initArticleFeedManager() {
  const feedContainer = document.getElementById('articles-feed-container');
  const sentinel = document.getElementById('scroll-sentinel');
  const spinner = document.getElementById('feed-loading-spinner');
  const loadMoreBtn = document.getElementById('manual-load-more-btn');
  const searchInput = document.getElementById('live-search-input');
  const heroSearchInput = document.getElementById('hero-search-input');
  const resultCountBadge = document.getElementById('result-count-badge');

  if (!feedContainer) return;

  let currentPage = 1;
  let hasNextPage = feedContainer.getAttribute('data-has-next') === 'true';
  let isLoading = false;
  let currentCategory = feedContainer.getAttribute('data-category') || '';
  let currentQuery = feedContainer.getAttribute('data-query') || '';

  // Setup Intersection Observer for dynamic scroll loading
  if (sentinel && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting && hasNextPage && !isLoading) {
          loadMoreArticles();
        }
      });
    }, { rootMargin: '250px' });

    observer.observe(sentinel);
  }

  if (loadMoreBtn) {
    loadMoreBtn.addEventListener('click', () => {
      if (hasNextPage && !isLoading) {
        loadMoreArticles();
      }
    });
  }

  function loadMoreArticles() {
    if (isLoading || !hasNextPage) return;
    isLoading = true;
    showLoading(true);

    const nextPage = currentPage + 1;
    const url = `/articles/api/feed/?page=${nextPage}&q=${encodeURIComponent(currentQuery)}&category=${encodeURIComponent(currentCategory)}`;

    fetch(url, {
      headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.html) {
          // Append new cards inside feedContainer
          const tempDiv = document.createElement('div');
          tempDiv.innerHTML = data.html;
          while (tempDiv.firstChild) {
            feedContainer.appendChild(tempDiv.firstChild);
          }
        }
        currentPage = data.current_page;
        hasNextPage = data.has_next;
        updateSentinelVisibility();
      })
      .catch((err) => console.error('Error loading more articles:', err))
      .finally(() => {
        isLoading = false;
        showLoading(false);
      });
  }

  // Live search debouncing & visual feedback elements
  const searchFeedback = document.getElementById('live-search-feedback');
  const searchFeedbackText = document.getElementById('search-feedback-text');
  const searchFeedbackIcon = document.getElementById('search-feedback-icon');
  const searchScrollBtn = document.getElementById('search-scroll-to-results-btn');
  const articlesAnchor = document.getElementById('articles-heading-anchor');

  let searchTimeout = null;
  function handleSearchInput(value, shouldScroll = false) {
    clearTimeout(searchTimeout);
    currentQuery = value.trim();

    if (searchFeedback) {
      if (currentQuery) {
        searchFeedback.classList.remove('hidden');
        if (searchFeedbackText) searchFeedbackText.textContent = `در حال جستجوی «${currentQuery}»...`;
        if (searchFeedbackIcon) searchFeedbackIcon.className = 'w-2.5 h-2.5 rounded-full bg-brand-orange animate-ping';
      } else {
        searchFeedback.classList.add('hidden');
      }
    }

    searchTimeout = setTimeout(() => {
      currentPage = 1;
      executeSearch(shouldScroll);
    }, 280);
  }

  function scrollToResults() {
    if (articlesAnchor) {
      articlesAnchor.scrollIntoView({ behavior: 'smooth', block: 'start' });
      articlesAnchor.classList.add('ring-4', 'ring-brand-purple/40', 'bg-brand-purple/5', 'p-4', 'rounded-3xl');
      setTimeout(() => {
        articlesAnchor.classList.remove('ring-4', 'ring-brand-purple/40', 'bg-brand-purple/5', 'p-4', 'rounded-3xl');
      }, 2200);
    }
  }

  if (searchScrollBtn) {
    searchScrollBtn.addEventListener('click', () => scrollToResults());
  }

  // Bind input listeners
  [searchInput, heroSearchInput].forEach((inputEl) => {
    if (!inputEl) return;

    inputEl.addEventListener('input', (e) => {
      const val = e.target.value;
      if (searchInput && searchInput !== e.target) searchInput.value = val;
      if (heroSearchInput && heroSearchInput !== e.target) heroSearchInput.value = val;
      handleSearchInput(val, false);
    });

    // On Enter key: instantly search and smooth-scroll to results
    inputEl.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        clearTimeout(searchTimeout);
        currentQuery = inputEl.value.trim();
        executeSearch(true);
      }
    });
  });

  function executeSearch(autoScroll = false) {
    isLoading = true;
    showLoading(true);

    const url = `/articles/api/feed/?page=1&q=${encodeURIComponent(currentQuery)}&category=${encodeURIComponent(currentCategory)}`;

    fetch(url, {
      headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
      .then((res) => res.json())
      .then((data) => {
        feedContainer.innerHTML = data.html || `
          <div class="col-span-full py-16 text-center">
            <div class="inline-flex p-4 rounded-full bg-border-color/30 text-text-muted mb-4">
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
            </div>
            <h4 class="text-lg font-bold text-text-primary mb-1">هیچ مقاله‌ای یافت نشد</h4>
            <p class="text-sm text-text-muted">لطفاً عبارت دیگری را جستجو کنید یا دسته‌بندی دیگری انتخاب نمایید.</p>
          </div>
        `;
        currentPage = 1;
        hasNextPage = data.has_next;
        if (resultCountBadge) {
          resultCountBadge.textContent = `${data.total_count} مقاله موجود`;
        }
        updateSentinelVisibility();

        // Update Search Feedback Banner
        if (searchFeedback) {
          if (currentQuery) {
            searchFeedback.classList.remove('hidden');
            if (data.total_count > 0) {
              if (searchFeedbackText) {
                searchFeedbackText.innerHTML = `یافت شد: <strong class="text-brand-orange">${data.total_count} مقاله</strong> برای «${currentQuery}»`;
              }
              if (searchFeedbackIcon) {
                searchFeedbackIcon.className = 'w-2.5 h-2.5 rounded-full bg-emerald-500';
              }
              if (searchScrollBtn) {
                searchScrollBtn.classList.remove('hidden');
                searchScrollBtn.innerHTML = `
                  <span>مشاهده ${data.total_count} نتیجه</span>
                  <svg class="w-3.5 h-3.5 rotate-90" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
                `;
              }
              // If user pressed enter, or if autoScroll requested, scroll smoothly
              if (autoScroll) {
                scrollToResults();
              }
            } else {
              if (searchFeedbackText) {
                searchFeedbackText.textContent = `هیچ مقاله‌ای برای «${currentQuery}» یافت نشد.`;
              }
              if (searchFeedbackIcon) {
                searchFeedbackIcon.className = 'w-2.5 h-2.5 rounded-full bg-rose-500';
              }
              if (searchScrollBtn) {
                searchScrollBtn.classList.add('hidden');
              }
            }
          } else {
            searchFeedback.classList.add('hidden');
          }
        }
      })
      .catch((err) => console.error('Search error:', err))
      .finally(() => {
        isLoading = false;
        showLoading(false);
      });
  }

  function showLoading(show) {
    if (spinner) spinner.classList.toggle('hidden', !show);
    if (loadMoreBtn) loadMoreBtn.classList.toggle('opacity-50', show);
  }

  function updateSentinelVisibility() {
    if (sentinel) sentinel.classList.toggle('hidden', !hasNextPage);
    if (loadMoreBtn) loadMoreBtn.classList.toggle('hidden', !hasNextPage);
  }
}

/* ----------------------------------------------------
   4. Asynchronous Comment Submission (Progressive)
   ---------------------------------------------------- */
function initCommentAjaxHandler() {
  const commentForm = document.getElementById('article-comment-form');
  const commentsList = document.getElementById('comments-container');
  const commentCountEl = document.getElementById('comment-count-display');

  if (!commentForm) return;

  commentForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const submitBtn = commentForm.querySelector('button[type="submit"]');
    const textarea = commentForm.querySelector('textarea');
    if (!textarea || !textarea.value.trim()) return;

    const formData = new FormData(commentForm);
    formData.append('is_ajax', '1');

    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.classList.add('opacity-75');
    }

    fetch(commentForm.action, {
      method: 'POST',
      body: formData,
      headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.status === 'success' && data.comment_html) {
          if (commentsList) {
            const emptyNotice = document.getElementById('no-comments-notice');
            if (emptyNotice) emptyNotice.remove();

            const temp = document.createElement('div');
            temp.innerHTML = data.comment_html;
            const newComment = temp.firstElementChild;
            newComment.classList.add('animate-fade-in-up');
            commentsList.insertBefore(newComment, commentsList.firstChild);

            if (commentCountEl) {
              const currentNum = parseInt(commentCountEl.textContent.trim() || '0', 10);
              commentCountEl.textContent = (currentNum + 1).toString();
            }
          }
          textarea.value = '';
          showToast('دیدگاه شما با موفقیت ثبت و منتشر گردید.');
        } else if (data.errors) {
          showToast('خطا در ثبت دیدگاه. لطفاً متن دیدگاه را بررسی کنید.', true);
        }
      })
      .catch((err) => {
        console.error('Comment submission error:', err);
        showToast('مشکلی در برقراری ارتباط با سرور رخ داد.', true);
      })
      .finally(() => {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.classList.remove('opacity-75');
        }
      });
  });

  function showToast(message, isError = false) {
    const toast = document.createElement('div');
    toast.className = `fixed bottom-6 left-6 z-50 px-5 py-3 rounded-2xl shadow-2xl text-sm font-medium transition-all duration-300 transform translate-y-10 opacity-0 flex items-center gap-3 ${
      isError ? 'bg-red-600 text-white' : 'bg-emerald-600 text-white'
    }`;
    toast.innerHTML = `
      <span>${isError ? '⚠️' : '✓'}</span>
      <span>${message}</span>
    `;
    document.body.appendChild(toast);

    requestAnimationFrame(() => {
      toast.classList.remove('translate-y-10', 'opacity-0');
      toast.classList.add('translate-y-0', 'opacity-100');
    });

    setTimeout(() => {
      toast.classList.add('opacity-0', 'translate-y-4');
      setTimeout(() => toast.remove(), 400);
    }, 4000);
  }
}
