const form = document.getElementById("domainForm");
const input = document.getElementById("domainInput");
const results = document.getElementById("domainResults");

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const raw = input.value.trim().toLowerCase();
  const name = raw.replace(/[^a-z0-9-]/g, "").replace(/^-+|-+$/g, "");
  results.innerHTML = "";
  if (!name) {
    results.textContent = "أدخل اسمًا لاتينيًا صالحًا للعرض التجريبي.";
    return;
  }
  const suffixes = [".ye",".com.ye",".org.ye",".net.ye",".edu.ye",".gov.ye"];
  suffixes.forEach((suffix) => {
    const row = document.createElement("div");
    row.className = "result";
    row.innerHTML = `<span>${name}${suffix}</span><span class="badge">صيغة عرض فقط</span>`;
    results.appendChild(row);
  });
});
