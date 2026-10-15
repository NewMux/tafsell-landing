// Single place to update contact details before launch.
const SALES_EMAIL = "info@newmux.com";

document.getElementById("sales-email").textContent = SALES_EMAIL;
document.getElementById("year").textContent = String(new Date().getFullYear());

document.getElementById("demo-form").addEventListener("submit", event => {
  event.preventDefault();
  const form = event.currentTarget;
  const data = new FormData(form);
  const name = data.get("name") || "";
  const shopName = data.get("shopName") || "";
  const email = data.get("email") || "";
  const phone = data.get("phone") || "";
  const message = data.get("message") || "";

  const subject = `Demo request: ${shopName || name}`;
  const bodyLines = [
    `Name: ${name}`,
    `Shop / business name: ${shopName}`,
    `Email: ${email}`,
    phone ? `Phone: ${phone}` : null,
    "",
    message || "(no additional message)",
  ].filter(line => line !== null);

  const params = new URLSearchParams({ subject, body: bodyLines.join("\n") });
  window.location.href = `mailto:${SALES_EMAIL}?${params.toString()}`;
});
