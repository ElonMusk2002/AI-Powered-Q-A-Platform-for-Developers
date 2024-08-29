// main.js

document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault();
      document.querySelector(this.getAttribute("href")).scrollIntoView({
        behavior: "smooth",
      });
    });
  });

  if (typeof Prism !== "undefined") {
    Prism.highlightAll();
  }

  const backToTopButton = document.createElement("button");
  backToTopButton.textContent = "↑";
  backToTopButton.classList.add("back-to-top");
  backToTopButton.style.display = "none";
  document.body.appendChild(backToTopButton);

  window.addEventListener("scroll", () => {
    if (window.pageYOffset > 100) {
      backToTopButton.style.display = "block";
    } else {
      backToTopButton.style.display = "none";
    }
  });

  backToTopButton.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });

  const animateOnScroll = () => {
    const elements = document.querySelectorAll(
      ".card, .user-stats, .ai-insights"
    );
    elements.forEach((element) => {
      const elementTop = element.getBoundingClientRect().top;
      const elementBottom = element.getBoundingClientRect().bottom;
      if (elementTop < window.innerHeight && elementBottom > 0) {
        element.classList.add("animate-in");
      }
    });
  };

  window.addEventListener("scroll", animateOnScroll);
  animateOnScroll();

  const forms = document.querySelectorAll("form");
  forms.forEach((form) => {
    form.addEventListener("submit", (e) => {
      const requiredFields = form.querySelectorAll("[required]");
      requiredFields.forEach((field) => {
        if (!field.value) {
          e.preventDefault();
          field.classList.add("error");
        } else {
          field.classList.remove("error");
        }
      });
    });
  });

  const menuToggle = document.createElement("button");
  menuToggle.textContent = "☰";
  menuToggle.classList.add("menu-toggle");
  const nav = document.querySelector("nav ul");
  nav.parentNode.insertBefore(menuToggle, nav);

  menuToggle.addEventListener("click", () => {
    nav.classList.toggle("show");
  });
});

const tagInput = document.getElementById("tags");
const suggestTagsButton = document.createElement("button");
suggestTagsButton.textContent = "Suggest Tags";
suggestTagsButton.classList.add("btn", "btn-secondary", "mt-2");
tagInput.parentNode.insertBefore(suggestTagsButton, tagInput.nextSibling);

suggestTagsButton.addEventListener("click", async (e) => {
  e.preventDefault();
  const title = document.getElementById("title").value;
  const body = document.getElementById("body").value;

  try {
    const response = await fetch("/api/suggest_tags", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ title, body }),
    });
    const data = await response.json();
    tagInput.value = data.tags.join(", ");
  } catch (error) {
    console.error("Error suggesting tags:", error);
  }
});

const topAnswer = document.querySelector('.answer[data-rank="1"]');
if (topAnswer) {
  topAnswer.classList.add("top-answer");
}
