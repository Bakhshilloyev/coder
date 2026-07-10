/* =========================================================
   FLORA MYTHICA — interaction layer
   ========================================================= */
(function () {
  "use strict";

  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const isTouch = window.matchMedia("(pointer: coarse)").matches;

  /* ---------- Loader ---------- */
  const loader = document.getElementById("loader");
  const loaderBar = document.getElementById("loaderBar");
  let progress = 0;
  const tick = setInterval(() => {
    progress = Math.min(progress + Math.random() * 16, 100);
    loaderBar.style.width = progress + "%";
    if (progress >= 100) clearInterval(tick);
  }, 130);
  window.addEventListener("load", () => {
    setTimeout(() => loader.classList.add("done"), 650);
  });

  /* ---------- Custom cursor ---------- */
  const cursor = document.getElementById("cursor");
  const dot = document.getElementById("cursorDot");
  if (!isTouch) {
    let cx = 0, cy = 0, dx = 0, dy = 0;
    window.addEventListener("mousemove", (e) => {
      cx = e.clientX; cy = e.clientY;
      dot.style.transform = `translate(${cx}px, ${cy}px) translate(-50%, -50%)`;
    });
    const render = () => {
      dx += (cx - dx) * 0.18;
      dy += (cy - dy) * 0.18;
      cursor.style.transform = `translate(${dx}px, ${dy}px) translate(-50%, -50%)`;
      requestAnimationFrame(render);
    };
    render();
    document.querySelectorAll("a, button, [data-tilt], [data-link]").forEach((el) => {
      el.addEventListener("mouseenter", () => cursor.classList.add("is-hover"));
      el.addEventListener("mouseleave", () => cursor.classList.remove("is-hover"));
    });
  }

  /* ---------- Nav scroll state + smooth anchor ---------- */
  const nav = document.getElementById("nav");
  const onScroll = () => {
    nav.classList.toggle("scrolled", window.scrollY > 40);
  };
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  document.querySelectorAll('a[href^="#"]').forEach((a) => {
    a.addEventListener("click", (e) => {
      const id = a.getAttribute("href");
      if (id.length > 1) {
        const target = document.querySelector(id);
        if (target) {
          e.preventDefault();
          target.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth" });
        }
      }
    });
  });

  /* ---------- Reveal on scroll ---------- */
  const revealEls = document.querySelectorAll("[data-reveal]");
  if ("IntersectionObserver" in window && !reduceMotion) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("in");
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
    revealEls.forEach((el) => io.observe(el));
  } else {
    revealEls.forEach((el) => el.classList.add("in"));
  }

  /* ---------- Parallax ---------- */
  const parallaxEls = document.querySelectorAll("[data-parallax]");
  if (!reduceMotion && parallaxEls.length) {
    let ticking = false;
    window.addEventListener("scroll", () => {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(() => {
        const y = window.scrollY;
        parallaxEls.forEach((el) => {
          const speed = parseFloat(el.dataset.parallax) || 0.1;
          el.style.transform = `translate3d(0, ${y * speed * -0.4}px, 0)`;
        });
        ticking = false;
      });
    }, { passive: true });
  }

  /* ---------- Card tilt + glow follow ---------- */
  if (!isTouch && !reduceMotion) {
    document.querySelectorAll("[data-tilt]").forEach((card) => {
      card.addEventListener("mousemove", (e) => {
        const r = card.getBoundingClientRect();
        const px = (e.clientX - r.left) / r.width;
        const py = (e.clientY - r.top) / r.height;
        card.style.setProperty("--mx", px * 100 + "%");
        card.style.setProperty("--my", py * 100 + "%");
        const rx = (py - 0.5) * -8;
        const ry = (px - 0.5) * 10;
        card.style.transform = `perspective(900px) rotateX(${rx}deg) rotateY(${ry}deg) translateY(-6px)`;
      });
      card.addEventListener("mouseleave", () => {
        card.style.transform = "";
      });
    });
  }

  /* ---------- Count-up stats ---------- */
  const stats = document.querySelectorAll(".stat__num");
  const animateCount = (el) => {
    const target = parseInt(el.dataset.count, 10) || 0;
    const dur = 1400;
    const start = performance.now();
    const step = (now) => {
      const p = Math.min((now - start) / dur, 1);
      const eased = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(target * eased).toLocaleString();
      if (p < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };
  if ("IntersectionObserver" in window && !reduceMotion) {
    const so = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) { animateCount(entry.target); so.unobserve(entry.target); }
      });
    }, { threshold: 0.6 });
    stats.forEach((s) => so.observe(s));
  } else {
    stats.forEach((s) => (s.textContent = parseInt(s.dataset.count, 10).toLocaleString()));
  }

  /* ---------- Falling petals in hero ---------- */
  const petals = document.getElementById("petals");
  if (petals && !reduceMotion) {
    const colors = ["#7ad29b", "#f6c6e6", "#e8d39a", "#f2a0a0", "#a9d4f2"];
    const makePetal = () => {
      const p = document.createElement("span");
      const size = 6 + Math.random() * 10;
      p.style.cssText = `
        position:absolute; top:-20px; left:${Math.random() * 100}%;
        width:${size}px; height:${size * 0.5}px; border-radius:50% 0 50% 0;
        background:${colors[Math.floor(Math.random() * colors.length)]};
        opacity:${0.25 + Math.random() * 0.4}; filter:blur(.4px);
        animation:fall ${8 + Math.random() * 9}s linear infinite;
        transform:rotate(${Math.random() * 360}deg);`;
      petals.appendChild(p);
      setTimeout(() => p.remove(), 18000);
    };
    for (let i = 0; i < 22; i++) setTimeout(makePetal, i * 320);
    setInterval(makePetal, 900);

    const style = document.createElement("style");
    style.textContent =
      "@keyframes fall { to { transform: translateY(110vh) rotate(540deg); opacity:.1; } }";
    document.head.appendChild(style);
  }

  /* ---------- CTA form ---------- */
  const form = document.getElementById("ctaForm");
  const note = document.getElementById("ctaNote");
  if (form) {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const input = form.querySelector("input");
      if (input.value && input.checkValidity()) {
        note.hidden = false;
        form.reset();
      }
    });
  }
})();
