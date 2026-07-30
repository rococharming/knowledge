function setFeedback(host, ok, message) {
  const feedback = host.querySelector(".feedback");
  if (!feedback) return;
  feedback.textContent = message;
  feedback.className = ok ? "feedback ok" : "feedback bad";
}

document.querySelectorAll("[data-quiz]").forEach((quiz) => {
  quiz.querySelectorAll("button[data-answer]").forEach((button) => {
    button.addEventListener("click", () => {
      const ok = button.dataset.answer === "true";
      setFeedback(quiz, ok, ok ? quiz.dataset.ok : quiz.dataset.bad);
    });
  });
});

document.querySelectorAll("[data-checklist]").forEach((block) => {
  const button = block.querySelector(".check-button");
  const input = block.querySelector("textarea");
  if (!button || !input) return;

  button.addEventListener("click", () => {
    const required = (block.dataset.required || "").split(",").map((item) => item.trim()).filter(Boolean);
    const text = input.value.toLowerCase();
    const missing = required.filter((item) => !text.includes(item.toLowerCase()));
    setFeedback(block, missing.length === 0, missing.length === 0
      ? block.dataset.ok
      : `${block.dataset.bad} 还缺：${missing.join("、")}`);
  });
});
