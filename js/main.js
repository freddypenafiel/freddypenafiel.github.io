// ==============================
// TEMA OSCURO / CLARO
// ==============================
const temaBtn = document.getElementById('tema-btn');
const body = document.body;

// Cargar tema guardado
const temaGuardado = localStorage.getItem('tema');
if (temaGuardado === 'oscuro') {
    body.classList.add('modo-oscuro');
}

temaBtn.addEventListener('click', () => {
    body.classList.toggle('modo-oscuro');
    const temaActual = body.classList.contains('modo-oscuro') ? 'oscuro' : 'claro';
    localStorage.setItem('tema', temaActual);
});

// ==============================
// NAVBAR AL HACER SCROLL
// ==============================
const navbar = document.getElementById('navbar');

window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// ==============================
// MENÚ MÓVIL
// ==============================
const menuToggle = document.getElementById('menu-toggle');
const mobileMenu = document.getElementById('mobile-menu');
const mobileLinks = document.querySelectorAll('.mobile-link');

menuToggle.addEventListener('click', () => {
    mobileMenu.classList.toggle('open');
});

mobileLinks.forEach(link => {
    link.addEventListener('click', () => {
        mobileMenu.classList.remove('open');
    });
});

// Cerrar menú al hacer click fuera
document.addEventListener('click', (e) => {
    if (!menuToggle.contains(e.target) && !mobileMenu.contains(e.target)) {
        mobileMenu.classList.remove('open');
    }
});

// ==============================
// ANIMACIONES AL HACER SCROLL
// ==============================
const animados = document.querySelectorAll('.animate-up');

const observador = new IntersectionObserver((entradas) => {
    entradas.forEach(entrada => {
        if (entrada.isIntersecting) {
            entrada.target.classList.add('visible');
        }
    });
}, {
    threshold: 0.1,
    rootMargin: '0px 0px -40px 0px'
});

animados.forEach(el => observador.observe(el));

// ==============================
// FORMULARIO DE CONTACTO
// ==============================
const form = document.getElementById('contacto-form');
const formNota = document.getElementById('form-nota');

form.addEventListener('submit', (e) => {
    e.preventDefault();

    const nombre = document.getElementById('nombre').value.trim();
    const email = document.getElementById('email').value.trim();
    const mensaje = document.getElementById('mensaje').value.trim();

    if (!nombre || !email || !mensaje) {
        formNota.style.color = '#ef4444';
        formNota.textContent = 'Por favor completa todos los campos.';
        return;
    }

    // Enviar por WhatsApp como alternativa (sin backend)
    const texto = encodeURIComponent(`Hola Freddy 👋\n\nMe llamo *${nombre}* (${email})\n\n${mensaje}`);
    const whatsappUrl = `https://wa.me/593998952547?text=${texto}`;

    formNota.style.color = '#22c55e';
    formNota.textContent = '✓ Redirigiendo a WhatsApp...';

    setTimeout(() => {
        window.open(whatsappUrl, '_blank');
        form.reset();
        formNota.textContent = '';
    }, 1200);
});

// ==============================
// NAVEGACIÓN ACTIVA AL SCROLL
// ==============================
const secciones = document.querySelectorAll('section[id]');
const navLinks = document.querySelectorAll('.nav-links a');

window.addEventListener('scroll', () => {
    let actual = '';
    secciones.forEach(sec => {
        const top = sec.offsetTop - 100;
        if (window.scrollY >= top) {
            actual = sec.getAttribute('id');
        }
    });

    navLinks.forEach(link => {
        link.style.color = '';
        if (link.getAttribute('href') === `#${actual}`) {
            link.style.color = 'var(--accent)';
        }
    });
});
