// Layout audit for the figures, run in a browser console on a rendered figN.html.
// Reports, in mm: each panel's free space on every side (content vs padding box), elements that
// overflow their parent box, text that is clipped, and sibling gaps that differ inside one container.
function audit() {
  const MMPX = 96 / 25.4, mm = (v) => Math.round((v / MMPX) * 10) / 10;
  const fig = document.getElementById("fig"), F = fig.getBoundingClientRect();
  const name = (e) => (e.id ? "#" + e.id : "") + (e.className && typeof e.className === "string" ? "." + e.className.trim().split(/\s+/).join(".") : "") || e.tagName.toLowerCase();
  const path = (e) => { const p = []; while (e && e !== fig) { p.unshift(name(e)); e = e.parentElement; } return p.slice(-3).join(" > "); };
  const out = { panels: [], overflow: [], clipped: [], gaps: [] };
  const visible = (e) => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 && getComputedStyle(e).visibility !== "hidden"; };

  for (const p of fig.querySelectorAll(".panel")) {
    const R = p.getBoundingClientRect(), cs = getComputedStyle(p);
    const pad = { t: parseFloat(cs.paddingTop) + parseFloat(cs.borderTopWidth), b: parseFloat(cs.paddingBottom) + parseFloat(cs.borderBottomWidth), l: parseFloat(cs.paddingLeft) + parseFloat(cs.borderLeftWidth), r: parseFloat(cs.paddingRight) + parseFloat(cs.borderRightWidth) };
    let u = { t: Infinity, b: -Infinity, l: Infinity, r: -Infinity };
    for (const e of p.querySelectorAll("*")) {
      if (!visible(e) || e.closest("svg") && e.tagName !== "svg") continue;
      if (e.children.length && getComputedStyle(e).backgroundColor === "rgba(0, 0, 0, 0)" && getComputedStyle(e).borderTopStyle === "none") continue; // pure layout wrappers
      const r = e.getBoundingClientRect();
      u = { t: Math.min(u.t, r.top), b: Math.max(u.b, r.bottom), l: Math.min(u.l, r.left), r: Math.max(u.r, r.right) };
    }
    out.panels.push({ panel: p.querySelector(".ptitle b")?.textContent, size: [mm(R.width), mm(R.height)],
      free: { top: mm(u.t - R.top - pad.t), bottom: mm(R.bottom - pad.b - u.b), left: mm(u.l - R.left - pad.l), right: mm(R.right - pad.r - u.r) } });
  }

  for (const e of fig.querySelectorAll(".panel *")) {
    if (!visible(e) || e.closest("svg")) continue;
    const par = e.parentElement; if (!par || par.closest("svg")) continue;
    const r = e.getBoundingClientRect(), q = par.getBoundingClientRect(), pcs = getComputedStyle(par);
    const over = Math.max(q.left - r.left, r.right - q.right, q.top - r.top, r.bottom - q.bottom);
    if (over > 0.3 * MMPX && pcs.display !== "contents") out.overflow.push({ el: path(e), by: mm(over), text: (e.textContent || "").trim().slice(0, 40) });
    if ((e.scrollWidth > e.clientWidth + 1 || e.scrollHeight > e.clientHeight + 1) && ["hidden", "clip"].includes(getComputedStyle(e).overflow) && e.clientWidth)
      out.clipped.push({ el: path(e), text: (e.textContent || "").trim().slice(0, 40) });
  }

  // flex/grid containers whose consecutive visible children sit at uneven vertical gaps
  for (const c of fig.querySelectorAll(".panel *")) {
    if (c.closest("svg")) continue;
    const d = getComputedStyle(c).display; if (!/flex|grid|block/.test(d)) continue;
    const kids = [...c.children].filter(visible).map((k) => k.getBoundingClientRect());
    if (kids.length < 3) continue;
    const col = kids.every((k, i) => !i || k.top >= kids[i - 1].bottom - 1);
    if (!col) continue;
    const gaps = kids.slice(1).map((k, i) => mm(k.top - kids[i].bottom));
    if (Math.max(...gaps) - Math.min(...gaps) > 0.6) out.gaps.push({ el: path(c), gaps });
  }
  return out;
}
