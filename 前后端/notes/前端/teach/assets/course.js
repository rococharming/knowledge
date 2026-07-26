(function () {
  const root = document.documentElement;
  const storedTheme = localStorage.getItem("course-theme");
  const initialTheme = storedTheme || "wood";

  function setTheme(theme) {
    root.dataset.theme = theme;
    localStorage.setItem("course-theme", theme);
    document.querySelectorAll("[data-theme-choice]").forEach((button) => {
      button.setAttribute("aria-pressed", String(button.dataset.themeChoice === theme));
    });
  }

  document.addEventListener("DOMContentLoaded", () => {
    setTheme(initialTheme);

    document.querySelectorAll("[data-theme-choice]").forEach((button) => {
      button.addEventListener("click", () => setTheme(button.dataset.themeChoice));
    });

    document.querySelectorAll("[data-quiz]").forEach((quiz) => {
      const button = quiz.querySelector("[data-check-answer]");
      const feedback = quiz.querySelector("[data-feedback]");
      const name = quiz.dataset.quiz;
      const answer = quiz.dataset.answer;

      button.addEventListener("click", () => {
        const selected = quiz.querySelector(`input[name="${name}"]:checked`);
        feedback.classList.remove("is-right", "is-wrong");

        if (!selected) {
          feedback.textContent = "先选一个答案，再检查。";
          feedback.classList.add("is-wrong");
          return;
        }

        if (selected.value === answer) {
          feedback.textContent = quiz.dataset.rightMessage || "答对了。";
          feedback.classList.add("is-right");
        } else {
          feedback.textContent = quiz.dataset.wrongMessage || "再想想，然后重新选择。";
          feedback.classList.add("is-wrong");
        }
      });
    });
  });
})();
