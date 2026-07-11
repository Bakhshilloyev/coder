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

  /* ---------- Specimen modal ---------- */
  const specimens = {
    yggdrasil: {
      idx: "01", name: "Yggdrasil", tag: "The World Ash",
      desc: "A column of green fire holding nine realms aloft, its roots drinking from the wells of fate. The ash does not grow so much as it listens — every branch a road the gods have walked, every root a question the dead still ask. To sit beneath it is to hear the weather of other worlds.",
      facts: [["Realm", "Asgard's Canopy"], ["Lifespan", "Eternal"], ["Element", "Sky & Root"], ["Keeper", "The Norns"]]
    },
    lotus: {
      idx: "02", name: "Lotus of Eternity", tag: "The Unfolding",
      desc: "Born of still water at the world's first dawn, it opens and closes the cosmos with a single breath. Each petal is a season the universe has not yet lived; each closing, a secret it chooses to keep. Drink from its cup, the old texts warn, and you will forget every sorrow — and every name.",
      facts: [["Realm", "The Still Lakes"], ["Bloom", "At first dawn"], ["Element", "Water & Light"], ["Keeper", "The Dawn Maidens"]]
    },
    mandrake: {
      idx: "03", name: "Mandrake", tag: "The Screaming Root",
      desc: "Pulled from the earth at midnight, it cries a sound no living ear should survive to repeat. The wise bind its stem to a fleeing dog and cover their ears with wax. What remains is a root shaped like a sleeping child — and a power that bends luck, love, and the door between life and death.",
      facts: [["Realm", "Midnight Fields"], ["Harvest", "At midnight"], ["Element", "Earth & Voice"], ["Keeper", "The Root-Witch"]]
    },
    amanita: {
      idx: "04", name: "Amanita", tag: "The Seer's Cap",
      desc: "Beneath its spotted crown, the veil between worlds grows thin enough to walk through. The fae wear it as a lamp; the shaman as a key. One bite and the forest begins to speak in colours, the stones to hum, and the self to loosen its grip on what is real.",
      facts: [["Realm", "The Fae Clearing"], ["Use", "The thinned veil"], ["Element", "Spore & Dream"], ["Keeper", "The Fae"]]
    },
    baobab: {
      idx: "05", name: "Baobab of Souls", tag: "The Upside-Down Tree",
      desc: "Planted by the gods and flung to earth, it keeps its roots in the sky and its memory in the soil. Elders gather beneath its hollow trunk to settle disputes and to listen — for the baobab remembers every story told in its shade, and forgets none of them.",
      facts: [["Realm", "Savanna of Memory"], ["Form", "Roots in sky"], ["Element", "Memory & Time"], ["Keeper", "The Elders"]]
    },
    narcissus: {
      idx: "06", name: "Narcissus", tag: "The Mirror Bloom",
      desc: "It blooms once above still water, and whoever meets its gaze forgets the shore entirely. The flower does not seduce — it simply reflects, and the viewer drowns in the sweetness of their own face. Even the gods have lingered too long at its glassy pool.",
      facts: [["Realm", "The Glass Pool"], ["Bloom", "Once only"], ["Element", "Mirror & Water"], ["Keeper", "The Drowned"]]
    }
  };

  const modal = document.getElementById("modal");
  const modalArt = document.getElementById("modalArt");
  const mIdx = document.getElementById("modalIdx");
  const mName = document.getElementById("modalName");
  const mTag = document.getElementById("modalTag");
  const mDesc = document.getElementById("modalDesc");
  const mFacts = document.getElementById("modalFacts");

  const openModal = (key) => {
    const s = specimens[key];
    if (!s || !modal) return;
    const card = document.querySelector(`.card[data-key="${key}"]`);
    const accent = card ? card.style.getPropertyValue("--accent") : "#d9b978";
    modal.style.setProperty("--accent", accent);
    const svg = card ? card.querySelector(".art-svg").cloneNode(true) : null;
    modalArt.innerHTML = "";
    if (svg) modalArt.appendChild(svg);
    mIdx.textContent = s.idx;
    mName.textContent = s.name;
    mTag.textContent = s.tag;
    mDesc.textContent = s.desc;
    mFacts.innerHTML = s.facts
      .map((f) => `<li><span>${f[0]}</span><span>${f[1]}</span></li>`)
      .join("");
    modal.classList.add("open");
    modal.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
  };
  const closeModal = () => {
    if (!modal) return;
    modal.classList.remove("open");
    modal.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
  };

  document.querySelectorAll(".card[data-key]").forEach((card) => {
    card.style.cursor = "none";
    card.addEventListener("click", () => openModal(card.dataset.key));
    card.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); openModal(card.dataset.key); }
    });
    card.setAttribute("tabindex", "0");
    card.setAttribute("role", "button");
  });
  if (modal) {
    modal.querySelectorAll("[data-close]").forEach((el) => el.addEventListener("click", closeModal));
    window.addEventListener("keydown", (e) => { if (e.key === "Escape") closeModal(); });
  }

  /* ---------- Back to top ---------- */
  const totop = document.getElementById("totop");
  if (totop) {
    window.addEventListener("scroll", () => {
      totop.classList.toggle("show", window.scrollY > 700);
    }, { passive: true });
    totop.addEventListener("click", () => {
      window.scrollTo({ top: 0, behavior: reduceMotion ? "auto" : "smooth" });
    });
  }
})();
