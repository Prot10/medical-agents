// Shared helpers: inline Tabler icons, load the figure data, draw connector arrows between
// elements once layout is final. The build waits for `document.body.dataset.ready`.

const MM = 96 / 25.4; // CSS px per mm

async function inlineIcons(root = document) {
  const nodes = [...root.querySelectorAll(".ic[data-i]")];
  const cache = {};
  await Promise.all(nodes.map(async (n) => {
    const name = n.dataset.i;
    cache[name] ??= fetch(`assets/icons/${name}.svg`).then((r) => r.text());
    n.innerHTML = (await cache[name]).replace(/class="[^"]*"/, "").replace(/width="24"\s+height="24"/, "");
  }));
}

function el(tag, attrs = {}, parent) {
  const svgTags = ["svg", "path", "line", "circle", "rect", "text", "g", "polyline", "marker", "defs", "tspan"];
  const e = svgTags.includes(tag) ? document.createElementNS("http://www.w3.org/2000/svg", tag) : document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === "text") e.textContent = v;
    else if (k === "html") e.innerHTML = v;
    else e.setAttribute(k, v);
  }
  if (parent) parent.appendChild(e);
  return e;
}

// One SVG overlay per figure for connectors drawn between laid-out elements.
function overlay(fig) {
  const svg = el("svg", { class: "arrow", style: "left:0;top:0;width:100%;height:100%" }, fig);
  const defs = el("defs", {}, svg);
  for (const [id, color] of Object.entries({ a: "#48484e", g: "#2a9fb0", b: "#0033A0", r: "#E15E32", p: "#6E2466", o: "#1C446A", d: "#a9a9b0" })) {
    const m = el("marker", { id: `m-${id}`, viewBox: "0 0 10 10", refX: 8, refY: 5, markerWidth: 5.5, markerHeight: 5.5, orient: "auto-start-reverse", markerUnits: "userSpaceOnUse" }, defs);
    el("path", { d: "M0.5,0.8 L9,5 L0.5,9.2 z", fill: color }, m);
  }
  return svg;
}

function anchor(fig, node, side) {
  const f = fig.getBoundingClientRect(), r = node.getBoundingClientRect();
  const x = { l: r.left, r: r.right, c: (r.left + r.right) / 2 }, y = { t: r.top, b: r.bottom, m: (r.top + r.bottom) / 2 };
  const map = { l: [x.l, y.m], r: [x.r, y.m], t: [x.c, y.t], b: [x.c, y.b] };
  const [px, py] = map[side];
  return [px - f.left, py - f.top];
}

// connect(svg, fig, fromNode, "r", toNode, "l", {color:"a", dash:false, bend:0, gap:1})
function connect(svg, fig, a, sa, b, sb, o = {}) {
  let [x1, y1] = anchor(fig, a, sa), [x2, y2] = anchor(fig, b, sb);
  const g = (o.gap ?? 0.8) * MM;
  const off = { l: [-g, 0], r: [g, 0], t: [0, -g], b: [0, g] };
  x1 += off[sa][0]; y1 += off[sa][1]; x2 += off[sb][0]; y2 += off[sb][1];
  if (o.level === "a") y2 = y1; if (o.level === "b") y1 = y2;
  if (o.dy1) y1 += o.dy1 * MM; if (o.dy2) y2 += o.dy2 * MM;
  if (o.dx1) x1 += o.dx1 * MM; if (o.dx2) x2 += o.dx2 * MM;
  let d;
  if (o.elbow === "h") { const mx = (x1 + x2) / 2; d = `M${x1},${y1} C${mx},${y1} ${mx},${y2} ${x2},${y2}`; }
  else if (o.elbow === "v") { const my = (y1 + y2) / 2; d = `M${x1},${y1} C${x1},${my} ${x2},${my} ${x2},${y2}`; }
  else d = `M${x1},${y1} L${x2},${y2}`;
  const color = { a: "#48484e", g: "#2a9fb0", b: "#0033A0", r: "#E15E32", p: "#6E2466", o: "#1C446A", d: "#a9a9b0" }[o.color ?? "a"];
  el("path", { d, fill: "none", stroke: color, "stroke-width": o.w ?? 0.75, "stroke-dasharray": o.dash ? "2.2 2" : "none", "marker-end": o.head === false ? "" : `url(#m-${o.color ?? "a"})`, "marker-start": o.both ? `url(#m-${o.color ?? "a"})` : "" }, svg);
  return [x1, y1, x2, y2];
}

// Every arrow in both figures: one stroke, one head (tip on the target point, the line stops at
// its base), orthogonal segments with rounded corners.
const ARROW = { w: 0.75, r: 1.2, head: 1.2, half: 0.6, gap: 0.9 }; // stroke in px, the rest in mm

function boxOf(fig, n) {
  const f = fig.getBoundingClientRect(), r = n.getBoundingClientRect();
  return { l: r.left - f.left, r: r.right - f.left, t: r.top - f.top, b: r.bottom - f.top, cx: (r.left + r.right) / 2 - f.left, cy: (r.top + r.bottom) / 2 - f.top };
}

// route(svg, [[x,y], ...], {color, dash, head, both}) draws an orthogonal arrow with rounded corners.
function route(svg, pts, o = {}) {
  const r = ARROW.r * MM, c = o.color ?? "a";
  const color = { a: "#48484e", g: "#2a9fb0", b: "#0033A0", r: "#E15E32", p: "#6E2466", o: "#1C446A", d: "#a9a9b0" }[c];
  pts = pts.map((p) => [...p]);
  const heads = [];
  const head = (tip, from) => {
    const d = Math.hypot(tip[0] - from[0], tip[1] - from[1]) || 1, ux = (tip[0] - from[0]) / d, uy = (tip[1] - from[1]) / d;
    const base = [tip[0] - ux * ARROW.head * MM, tip[1] - uy * ARROW.head * MM], h = ARROW.half * MM;
    heads.push(`M${tip[0]},${tip[1]} L${base[0] - uy * h},${base[1] + ux * h} L${base[0] + uy * h},${base[1] - ux * h} Z`);
    return base;
  };
  if (o.head !== false) pts[pts.length - 1] = head(pts.at(-1), pts.at(-2));
  if (o.both) pts[0] = head(pts[0], pts[1]);
  let d = `M${pts[0][0]},${pts[0][1]}`;
  for (let i = 1; i < pts.length - 1; i++) {
    const [px, py] = pts[i - 1], [x, y] = pts[i], [nx, ny] = pts[i + 1];
    const k1 = Math.min(r, Math.hypot(x - px, y - py) / 2), k2 = Math.min(r, Math.hypot(nx - x, ny - y) / 2);
    const ux = Math.sign(x - px), uy = Math.sign(y - py), vx = Math.sign(nx - x), vy = Math.sign(ny - y);
    d += ` L${x - ux * k1},${y - uy * k1} Q${x},${y} ${x + vx * k2},${y + vy * k2}`;
  }
  d += ` L${pts.at(-1)[0]},${pts.at(-1)[1]}`;
  const g = el("g", {}, svg);
  el("path", { d, fill: "none", stroke: color, "stroke-width": ARROW.w, "stroke-dasharray": o.dash ? "2.2 2" : "none" }, g);
  for (const h of heads) el("path", { d: h, fill: color }, g);
  return g;
}

// link(svg, fig, a, b, o): straight arrow from box a to box b, horizontal when they sit side by
// side, vertical when stacked, placed at the middle of the range the two boxes share.
function link(svg, fig, a, b, o = {}) {
  const A = boxOf(fig, a), B = boxOf(fig, b), g = (o.gap ?? ARROW.gap) * MM;
  const mid = (p, q, r, s) => (Math.max(p, r) + Math.min(q, s)) / 2;
  if (A.r <= B.l || B.r <= A.l) {
    const y = o.y ?? mid(A.t, A.b, B.t, B.b), fwd = A.r <= B.l;
    return route(svg, [[fwd ? A.r + g : A.l - g, y], [fwd ? B.l - g : B.r + g, y]], o);
  }
  const x = o.x ?? mid(A.l, A.r, B.l, B.r), down = A.b <= B.t;
  return route(svg, [[x, down ? A.b + g : A.t - g], [x, down ? B.t - g : B.b + g]], o);
}

function label(svg, x, y, text, o = {}) {
  return el("text", { x, y, "text-anchor": o.anchor ?? "middle", "font-size": o.size ?? "5.2pt", fill: o.fill ?? "#48484e", "font-family": "Arial", transform: o.rotate ? `rotate(${o.rotate} ${x} ${y})` : "", text }, svg);
}

// Replace SVG arrow markers with plain triangles, for tools that do not read <marker> (Figma import).
function flattenMarkers() {
  const k = 0.55; // marker scale: markerWidth 5.5 over a 10-unit viewBox
  for (const p of document.querySelectorAll("path[marker-end], path[marker-start]")) {
    const svg = p.ownerSVGElement, len = p.getTotalLength(), color = p.getAttribute("stroke");
    const head = (at, back) => {
      const a = p.getPointAtLength(at), b = p.getPointAtLength(back);
      const d = Math.hypot(a.x - b.x, a.y - b.y) || 1, ux = (a.x - b.x) / d, uy = (a.y - b.y) / d;
      const tip = [a.x + ux * k, a.y + uy * k], base = [a.x - ux * 7.5 * k, a.y - uy * 7.5 * k], w = 4.2 * k;
      el("path", { d: `M${tip} L${base[0] - uy * w},${base[1] + ux * w} L${base[0] + uy * w},${base[1] - ux * w} Z`, fill: color }, svg);
    };
    if ((p.getAttribute("marker-end") || "").startsWith("url")) head(len, Math.max(0, len - 1));
    if ((p.getAttribute("marker-start") || "").startsWith("url")) head(0, Math.min(len, 1));
    p.removeAttribute("marker-end"); p.removeAttribute("marker-start");
  }
  document.querySelectorAll("svg defs").forEach((d) => d.remove());
}

// Figma import: icons keep their look only with every presentation attribute on each shape
// (inherited stroke and currentColor are lost), and Arial has no 500/600 weights there.
function flattenForFigma() {
  for (const svg of document.querySelectorAll(".ic svg")) {
    const cs = getComputedStyle(svg), r = svg.getBoundingClientRect(), color = cs.color;
    svg.querySelectorAll('[stroke="none"]').forEach((n) => n.remove());
    for (const s of svg.querySelectorAll("path, circle, rect, line, polyline, polygon, ellipse")) {
      const fill = s.getAttribute("fill");
      s.setAttribute("fill", fill && fill !== "none" ? (fill === "currentColor" ? color : fill) : "none");
      s.setAttribute("stroke", s.getAttribute("stroke") === "none" ? "none" : color);
      s.setAttribute("stroke-width", parseFloat(cs.strokeWidth));
      s.setAttribute("stroke-linecap", "round"); s.setAttribute("stroke-linejoin", "round");
    }
    for (const a of ["fill", "stroke", "stroke-width", "stroke-linecap", "stroke-linejoin"]) svg.removeAttribute(a);
    svg.setAttribute("width", r.width); svg.setAttribute("height", r.height);
  }
  // SVG <text> lands in Figma's default font: replace each with HTML text on the same box.
  const fig = document.getElementById("fig"), F = fig.getBoundingClientRect();
  for (const t of [...document.querySelectorAll("#fig svg text")]) {
    const m = t.getScreenCTM(), scale = Math.hypot(m.a, m.b), angle = Math.atan2(m.b, m.a) * 180 / Math.PI;
    const r = t.getBoundingClientRect(), cs = getComputedStyle(t);
    const s = el("span", { text: t.textContent }, fig);
    Object.assign(s.style, { position: "absolute", fontFamily: "Arial", whiteSpace: "nowrap", lineHeight: "normal",
      fontSize: parseFloat(cs.fontSize) * scale + "px", color: cs.fill, opacity: cs.fillOpacity,
      left: (r.left + r.right) / 2 - F.left + "px", top: (r.top + r.bottom) / 2 - F.top + "px",
      transform: `translate(-50%, -50%)${Math.abs(angle) > 0.5 ? ` rotate(${angle}deg)` : ""}` });
    t.remove();
  }
  // Charts drawn in a mm viewBox: write their coordinates in px, since the import ignores viewBox.
  for (const svg of document.querySelectorAll("#fig svg[viewBox]")) {
    if (svg.closest(".ic")) continue;
    const vb = svg.viewBox.baseVal, w = vb.width, h = vb.height, k = svg.getBoundingClientRect().width / w;
    if (!w || Math.abs(k - 1) < 0.01) continue;
    for (const e of svg.querySelectorAll("*"))
      for (const a of ["x", "y", "width", "height", "rx", "cx", "cy", "r", "x1", "x2", "y1", "y2", "stroke-width"])
        if (e.hasAttribute(a)) e.setAttribute(a, parseFloat(e.getAttribute(a)) * k);
    svg.setAttribute("viewBox", `0 0 ${w * k} ${h * k}`);
  }
  for (const e of document.querySelectorAll("#fig *")) {
    const w = +getComputedStyle(e).fontWeight;
    if (w === 500 || w === 600) e.style.fontWeight = w === 600 ? "700" : "400";
  }
}

async function boot(render) {
  const data = await fetch("data/figures.json").then((r) => r.json());
  document.querySelector(".figure").dataset.style = new URLSearchParams(location.search).get("style") || "tint";
  render(data);
  await inlineIcons();
  await document.fonts.ready;
  if (window.afterLayout) window.afterLayout(data);
  if (new URLSearchParams(location.search).has("static")) { flattenMarkers(); flattenForFigma(); }
  document.body.dataset.ready = "1";
}
