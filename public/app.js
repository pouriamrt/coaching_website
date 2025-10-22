async function postJSON(url, data) {
  const res = await fetch(url, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(data)
  });
  return res.json();
}

function serialize(form) {
  const fd = new FormData(form);
  const out = {};
  for (const [k, v] of fd.entries()) out[k] = v;
  return out;
}

function wireForm(id, api, msgId) {
  const form = document.getElementById(id);
  const msg = document.getElementById(msgId);
  if (!form) return;
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const data = serialize(form);
    if (data.website) { msg.textContent = "Thanks!"; form.reset(); return; }
    msg.textContent = "Sending...";
    try {
      const res = await postJSON(api, data);
      msg.textContent = res.ok ? res.message : (res.error || "Something went wrong.");
      if (res.ok) form.reset();
    } catch {
      msg.textContent = "Network error.";
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  wireForm("contactForm", "/api/contact", "contactMsg");
  wireForm("intakeForm", "/api/intake", "intakeMsg");
  const nf = document.getElementById("newsletterForm");
  if (nf) {
    const nm = document.getElementById("newsletterMsg");
    nf.addEventListener("submit", async (e) => {
      e.preventDefault();
      const data = serialize(nf);
      if (data.website) { nm.textContent = "You're on the list!"; nf.reset(); return; }
      nm.textContent = "Adding...";
      try {
        const res = await postJSON("/api/newsletter", data);
        nm.textContent = res.ok ? res.message : (res.error || "Try again.");
        if (res.ok) nf.reset();
      } catch {
        nm.textContent = "Network error.";
      }
    });
  }
});
