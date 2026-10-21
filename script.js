// Single place to update contact details.
const SALES_EMAIL = "info@newmux.com";

// "Book a demo" requests go to the Tafsell app, which stores each one and
// emails it to SALES_EMAIL (Tailor-saas: server/_core/demoRequests.ts). Only
// tafsell.com may call it, so on a local preview point it at a local app.
const LOCAL = ["localhost", "127.0.0.1"].includes(window.location.hostname);
const DEMO_REQUEST_URL = `${LOCAL ? "http://localhost:3000" : "https://app.tafsell.com"}/api/public/demo-request`;

const LANGUAGE = document.documentElement.lang === "ar" ? "ar" : "en";

const COPY = {
  en: {
    sending: "Sending…",
    error: "We couldn't send your request. Please try again, or email us at ",
    rateLimited: "You've sent several requests already. Please email us at ",
  },
  ar: {
    sending: "جارٍ الإرسال…",
    error: "تعذّر إرسال طلبك. يرجى المحاولة مرة أخرى، أو مراسلتنا على ",
    rateLimited: "لقد أرسلت عدة طلبات بالفعل. يرجى مراسلتنا على ",
  },
}[LANGUAGE];

// Vercel Web Analytics (cookie-free). The script is served from this site
// once Web Analytics is enabled for the project; until then calls just queue.
window.va = window.va || function () { (window.vaq = window.vaq || []).push(arguments); };

for (const element of document.querySelectorAll("[data-sales-email]")) element.textContent = SALES_EMAIL;
document.getElementById("year").textContent = String(new Date().getFullYear());

const form = document.getElementById("demo-form");
const status = document.getElementById("demo-status");
const submit = form.querySelector('button[type="submit"]');
const submitLabel = submit.innerHTML;

function showError(prefix) {
  const link = document.createElement("a");
  link.href = `mailto:${SALES_EMAIL}`;
  link.textContent = SALES_EMAIL;
  status.replaceChildren(prefix, link, ".");
  status.hidden = false;
}

form.addEventListener("submit", async event => {
  event.preventDefault();
  const data = Object.fromEntries(new FormData(form));
  status.hidden = true;
  submit.disabled = true;
  submit.textContent = COPY.sending;
  try {
    const response = await fetch(DEMO_REQUEST_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ...data, language: LANGUAGE }),
    });
    if (!response.ok) {
      showError(response.status === 429 ? COPY.rateLimited : COPY.error);
      return;
    }
    window.va("event", { name: "Demo request", data: { language: LANGUAGE } });
    form.hidden = true;
    document.getElementById("demo-success").hidden = false;
    document.getElementById("demo-success").focus();
  } catch {
    showError(COPY.error);
  } finally {
    submit.disabled = false;
    submit.innerHTML = submitLabel;
  }
});
