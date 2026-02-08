/* ===========================
   COMPOSANTS RÉUTILISABLES
   =========================== */

class Component {
  static createIcon(name) {
    const icons = {
      network: `<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor"><circle cx="12" cy="12" r="3"/><circle cx="6" cy="6" r="2"/><circle cx="18" cy="6" r="2"/><circle cx="18" cy="18" r="2"/><circle cx="6" cy="18" r="2"/><line x1="9" y1="7" x2="15" y2="7"/><line x1="7" y1="9" x2="7" y2="15"/><line x1="17" y1="9" x2="17" y2="15"/><line x1="9" y1="17" x2="15" y2="17"/></svg>`,
      link: `<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>`,
      code: `<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor"><polyline points="16 18 22 12 16 6"></polyline><polyline points="8 6 2 12 8 18"></polyline></svg>`,
      server: `<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor"><rect x="2" y="2" width="20" height="8"/><rect x="2" y="14" width="20" height="8"/><line x1="6" y1="6" x2="6" y2="6.01"/><line x1="6" y1="18" x2="6" y2="18.01"/></svg>`,
      video: `<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor"><polygon points="23 7 16 12 23 17 23 7"></polygon><rect x="1" y="5" width="15" height="14" rx="2" ry="2"></rect></svg>`,
      chevronDown: `<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"></polyline></svg>`,
      github: `<svg class="icon" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v 3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>`,
      mail: `<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 5L2 7"/></svg>`,
      calendar: `<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>`,
      check: `<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor"><polyline points="20 6 9 17 4 12"></polyline></svg>`,
    };
    return icons[name] || '';
  }

  static createBadges(keywords) {
    if (!Array.isArray(keywords) || keywords.length === 0) {
      return `<div class="badge-container"><span class="badge">[Mots-clés à ajouter]</span></div>`;
    }
    return `<div class="badge-container">${keywords.map(k => `<span class="badge">${k}</span>`).join('')}</div>`;
  }

  static createAccordion(items, activeIndex = null) {
    return `<div class="accordion">
      ${items.map((item, idx) => `
        <div class="accordion-item">
          <div class="accordion-header ${activeIndex === idx ? 'active' : ''}" data-accordion-toggle data-index="${idx}">
            <span>${item.title}</span>
            <span class="accordion-toggle">▼</span>
          </div>
          <div class="accordion-content ${activeIndex === idx ? 'active' : ''}">
            <div class="accordion-body">${item.content}</div>
          </div>
        </div>
      `).join('')}
    </div>`;
  }

  static createCompetenceCard(competence) {
    return `
      <div class="card">
        <div style="font-size: 32px; margin-bottom: 12px;">
          ${competence.emoji || '📌'}
        </div>
        <h3>${competence.title}</h3>
        <a href="#competence-${competence.id}" class="btn btn-secondary btn-sm">
          Voir en détail
        </a>
      </div>
    `;
  }

  static createBreadcrumbs(items) {
    return `<div class="breadcrumbs">
      ${items.map((item, idx) => {
        if (idx === items.length - 1) {
          return `<span>${item.label}</span>`;
        }
        return `<a href="${item.href}">${item.label}</a><span>/</span>`;
      }).join('')}
    </div>`;
  }
}

/* ===========================
   EVENT LISTENERS
   =========================== */

function initAccordions() {
  const headers = document.querySelectorAll('[data-accordion-toggle]');
  headers.forEach(header => {
    header.addEventListener('click', () => {
      const content = header.nextElementSibling;
      const isActive = header.classList.contains('active');
      
      // Fermer tous les autres
      headers.forEach(h => {
        if (h !== header) {
          h.classList.remove('active');
          h.nextElementSibling.classList.remove('active');
        }
      });
      
      // Basculer celui-ci
      header.classList.toggle('active');
      content.classList.toggle('active');
    });
  });
}

function initMenuToggle() {
  const toggle = document.querySelector('.menu-toggle');
  const navLinks = document.querySelector('.nav-links');
  
  if (toggle) {
    toggle.addEventListener('click', () => {
      navLinks.classList.toggle('active');
    });
  }
}

function initDropdownMenu() {
  const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
  const dropdownItems = document.querySelectorAll('.dropdown-item');
  
  // Gestion du dropdown sur desktop (hover)
  // Gestion sur mobile (click)
  dropdownToggles.forEach(toggle => {
    toggle.addEventListener('click', (e) => {
      e.preventDefault();
      const parent = toggle.closest('.nav-dropdown');
      parent.classList.toggle('active');
    });
  });
  
  // Permettre le clic sur les items du dropdown
  dropdownItems.forEach(item => {
    item.addEventListener('click', (e) => {
      // Ne pas empêcher le comportement par défaut du lien
      const parent = item.closest('.nav-dropdown');
      if (parent) {
        parent.classList.remove('active');
      }
      
      // Fermer le menu mobile aussi
      const navLinks = document.querySelector('.nav-links');
      if (navLinks) {
        navLinks.classList.remove('active');
      }
    });
  });
}

function initNavigation() {
  const navLinks = document.querySelectorAll('.nav-link:not(.dropdown-toggle)');
  navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      const mobileNav = document.querySelector('.nav-links');
      if (mobileNav) {
        mobileNav.classList.remove('active');
      }
    });
  });
}

/* ===========================
   INITIALISATION
   =========================== */

document.addEventListener('DOMContentLoaded', () => {
  initMenuToggle();
  initDropdownMenu();
  initNavigation();
  initAccordions();
});
