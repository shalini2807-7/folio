
/* DARK MODE TOGGLE */

const themeToggle = document.querySelector('#theme-toggle');

themeToggle.addEventListener('click', () => {
  document.body.classList.toggle('dark');
  const isDark = document.body.classList.contains('dark');
  themeToggle.textContent = isDark ? '\u2600\uFE0F' : '\uD83C\uDF19'; // ☀️ or 🌙
});


/* BACK-TO-TOP BUTTON */

const toTop = document.querySelector('#to-top');

window.addEventListener('scroll', () => {
  if (window.scrollY > 300) {
    toTop.classList.add('show');
  } else {
    toTop.classList.remove('show');
  }
});

toTop.addEventListener('click', () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
});


/* SCROLL REVEAL */
const revealItems = document.querySelectorAll('.reveal');

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('is-visible');
      observer.unobserve(entry.target);
    }
  });
}, {
  threshold: 0.15 // fire when 15% of the element is visible
});

revealItems.forEach((item) => observer.observe(item));

document.addEventListener("DOMContentLoaded", () => {
  const buttons = document.querySelectorAll(".filter-btn");
  const cards = document.querySelectorAll(".projects-grid .card");
  const countDisplay = document.getElementById("project-count");

  buttons.forEach(button => {
    button.addEventListener("click", () => {
      // 1. Change active class highlight on buttons
      buttons.forEach(btn => btn.classList.remove("active"));
      button.classList.add("active");

      const filterValue = button.getAttribute("data-filter");
      let visibleCount = 0;

      // 2. Loop through all cards to hide or show them
      cards.forEach(card => {
        const cardCategory = card.getAttribute("data-category");

        if (filterValue === "all" || filterValue === cardCategory) {
          // Show card with a tiny delay to allow display property to reset smoothly
          card.style.display = "block";
          setTimeout(() => {
            card.classList.remove("hide");
          }, 10);
          visibleCount++;
        } else {
          // Hide card smoothly
          card.classList.add("hide");
          // Use setTimeout to wait for the CSS opacity transition to finish before display: none
          setTimeout(() => {
            if (card.classList.contains("hide")) {
              card.style.display = "none";
            }
          }, 400); // matches the 0.4s transition duration in CSS
        }
      });

      // 3. Update the text counter dynamically
      if (filterValue === "all") {
        countDisplay.textContent = `Showing all ${cards.length} projects`;
      } else {
        countDisplay.textContent = `Showing ${visibleCount} of ${cards.length} projects`;
      }
    });
  });
});
