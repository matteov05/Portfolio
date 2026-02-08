/* ===========================
   GESTION DE LA NAVIGATION
   =========================== */

class Router {
  constructor() {
    this.competences = [];
    this.currentPage = 'home';
    this.init();
  }

  async init() {
    await this.loadCompetences();
    this.setupRoutes();
    this.handleRoute();
    window.addEventListener('hashchange', () => this.handleRoute());
  }

  async loadCompetences() {
    try {
      const response = await fetch('./data/competences.json');
      const data = await response.json();
      this.competences = data.competences;
    } catch (error) {
      console.error('Erreur chargement données:', error);
    }
  }

  handleRoute() {
    const hash = window.location.hash.slice(1) || 'home';
    const [page, ...params] = hash.split('/');
    
    this.currentPage = page;
    this.showPage(page, params);
    this.updateNav(page);
  }

  updateNav(page) {
    const navLinks = document.querySelectorAll('.nav-link, .dropdown-item');
    navLinks.forEach(link => {
      link.classList.remove('active');
      const href = link.getAttribute('href');
      if (!href) return;
      
      // Nettoyer le href pour comparaison
      const hrefClean = href.replace('#', '');
      if ((page === 'home' && hrefClean === 'home') || 
          (page !== 'home' && hrefClean === page)) {
        link.classList.add('active');
      }
    });
  }

  showPage(page, params) {
    // Masquer toutes les pages
    const pages = document.querySelectorAll('[data-page]');
    pages.forEach(p => p.classList.remove('active'));
    
    // Afficher la page demandée
    const targetPage = document.querySelector(`[data-page="${page}"]`);
    if (targetPage) {
      targetPage.classList.add('active');
      window.scrollTo(0, 0);
    }
  }

  setupRoutes() {
    // Les liens avec href="#..." fonctionneront naturellement
    // Pas besoin d'intercepter les clics
    // Le gestionnaire 'hashchange' prendra le relais
  }
}

/* ===========================
   INITIALISATION APP
   =========================== */

let router;

document.addEventListener('DOMContentLoaded', () => {
  router = new Router();
  
  // Événements additionnels
  initSmoothScroll();
  initFormHandlers();
});

function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const href = this.getAttribute('href');
      if (href.length > 1 && href[1] !== '/') {
        e.preventDefault();
        const target = document.querySelector(href);
        if (target) {
          target.scrollIntoView({ behavior: 'smooth' });
        }
      }
    });
  });
}

function initFormHandlers() {
  // À implémenter: gestion de formulaires si nécessaire
  console.log('Form handlers ready');
}

/* ===========================
   UTILITAIRES
   =========================== */

function getCompetenceById(id) {
  return router.competences.find(c => c.id === parseInt(id));
}

function getCompetenceBySlug(slug) {
  return router.competences.find(c => c.slug === slug);
}
