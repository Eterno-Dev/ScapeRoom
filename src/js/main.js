// Redirección inmediata si se accede con parámetros de pista o código QR desde la raíz
const initialParams = new URLSearchParams(window.location.search);
if (initialParams.has("pista") || initialParams.has("c") || initialParams.has("code") || initialParams.has("token") || initialParams.has("p")) {
  window.location.replace("jugar/valparaiso/" + window.location.search + window.location.hash);
}

// Carrito en memoria. Al conectar pagos, sustituye checkout() por tu pasarela.
const cart = [];
const $ = (s) => document.querySelector(s);
const eur = (n) => n.toFixed(2).replace(".", ",") + " €";

function render() {
  const list = $("#cart-list");
  list.innerHTML = "";
  cart.forEach((p, i) => {
    const li = document.createElement("li");
    li.innerHTML = `<div>${p.name}<button data-i="${i}">Quitar</button></div><span>${eur(p.price)}</span>`;
    list.appendChild(li);
  });
  const total = cart.reduce((s, p) => s + p.price, 0);
  $("#cart-total").textContent = eur(total);
  $("#cart-count").textContent = cart.length;
  $("#fab-count").textContent = cart.length;
  $("#cart-empty").hidden = cart.length > 0;
  $("#checkout").disabled = cart.length === 0;
}

function toggle(open) {
  $("#cart").classList.toggle("open", open);
  $("#cart").setAttribute("aria-hidden", String(!open));
  $("#scrim").hidden = !open;
}

document.querySelectorAll(".folder .add").forEach((btn) =>
  btn.addEventListener("click", () => {
    const f = btn.closest(".folder");
    if (cart.some((p) => p.id === f.dataset.id)) return toggle(true); // un expediente se compra una vez
    cart.push({ id: f.dataset.id, name: f.dataset.name, price: parseFloat(f.dataset.price) });
    render();
    toggle(true);
  })
);
$("#cart-list").addEventListener("click", (e) => {
  if (e.target.dataset.i) { cart.splice(+e.target.dataset.i, 1); render(); }
});
$("#open-cart").addEventListener("click", () => toggle(true));
$("#close-cart").addEventListener("click", () => toggle(false));
$("#scrim").addEventListener("click", () => toggle(false));
document.addEventListener("keydown", (e) => e.key === "Escape" && toggle(false));
$("#checkout").addEventListener("click", () => alert("Aquí iría el pago. Conecta Stripe o Lemon Squeezy."));
document.querySelectorAll(".redact:not(.revealed-never)").forEach((b) =>
  b.addEventListener("click", () => b.classList.toggle("on"))
);
render();

// Dossiers apilados: se abre uno y los demás se pliegan
const list = document.querySelector("#cases-list");
document.querySelectorAll(".toggle, .tab-toggle").forEach((t) =>
  t.addEventListener("click", () => {
    const folder = t.closest(".folder");
    const main = folder.querySelector(".toggle");
    const willOpen = !folder.classList.contains("open");
    list.querySelectorAll(".folder.open").forEach((f) => {
      f.classList.remove("open");
      f.querySelector(".toggle").setAttribute("aria-expanded", "false");
      f.querySelector(".panel").inert = true;
    });
    if (willOpen) {
      folder.classList.add("open");
      main.setAttribute("aria-expanded", "true");
      folder.querySelector(".panel").inert = false;
      setTimeout(() => folder.scrollIntoView({ behavior: "smooth", block: "start" }), 60);
    }
    list.classList.toggle("has-open", willOpen);
  })
);

// Carrito flotante: aparece cuando la cabecera sale de la pantalla
const fab = $("#fab-cart");
fab.addEventListener("click", () => toggle(true));
new IntersectionObserver(([e]) => { fab.hidden = e.isIntersecting; }).observe(document.querySelector(".top"));
