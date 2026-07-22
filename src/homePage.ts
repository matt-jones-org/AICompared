/**
 * Home page for the AICompared server, styled to match the matt-jones.org
 * design system (the "Website about Nothing" baseball theme) so every page
 * across the site looks uniform. Self-contained: inline CSS, no external
 * assets, light/dark via prefers-color-scheme.
 */
export const HOME_PAGE_HTML = `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>AICompared | Matt Jones</title>
<style>
  :root {
    color-scheme: light dark;
    --paper:   #F2F4EC;
    --card:    #FBFCF7;
    --ink:     #171A12;
    --muted:   #5B6152;
    --line:    #C9CFBE;
    --stitch:  #CC3B2E;
    --grass:   #2F6B45;
    --shadow:  0 1px 0 rgba(23,26,18,.04), 0 12px 30px -18px rgba(23,26,18,.35);
    --maxw: 1080px;
    --f-display: "Helvetica Neue", "Arial Narrow", Arial, sans-serif;
    --f-body: ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    --f-mono: ui-monospace, "SF Mono", "Cascadia Mono", "Roboto Mono", Menlo, Consolas, monospace;
  }
  @media (prefers-color-scheme: dark) {
    :root {
      --paper:  #0D1310;
      --card:   #141B14;
      --ink:    #EDEFE6;
      --muted:  #9AA394;
      --line:   #2A3326;
      --stitch: #E4573F;
      --grass:  #4E9E6A;
      --shadow: 0 1px 0 rgba(0,0,0,.3), 0 18px 40px -22px rgba(0,0,0,.8);
    }
  }

  * { box-sizing: border-box; }
  body {
    margin: 0;
    background: var(--paper);
    color: var(--ink);
    font-family: var(--f-body);
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
    text-rendering: optimizeLegibility;
  }
  .wrap { max-width: var(--maxw); margin: 0 auto; padding: 0 24px; }

  a { color: inherit; }
  a:focus-visible, button:focus-visible, textarea:focus-visible {
    outline: 2px solid var(--stitch);
    outline-offset: 3px;
    border-radius: 2px;
  }

  .mono { font-family: var(--f-mono); }

  .stitch { height: 0; border-top: 2px dashed var(--stitch); opacity: .8; }

  header.bar {
    position: sticky; top: 0; z-index: 20;
    background: color-mix(in srgb, var(--paper) 88%, transparent);
    backdrop-filter: saturate(1.1) blur(8px);
    border-bottom: 1px solid var(--line);
  }
  .bar .wrap {
    display: flex; align-items: center; justify-content: space-between;
    height: 60px;
  }
  .wordmark {
    font-family: var(--f-display);
    font-weight: 800; letter-spacing: .14em; text-transform: uppercase;
    font-size: .95rem; text-decoration: none;
    display: inline-flex; align-items: center; gap: .5em;
  }
  .wordmark .ball {
    width: 15px; height: 15px; border-radius: 50%;
    background: var(--card);
    border: 1.5px solid var(--stitch);
    position: relative; display: inline-block;
  }
  .wordmark .ball::before, .wordmark .ball::after {
    content:""; position:absolute; inset:2px 4px;
    border:1px solid var(--stitch); border-top:0; border-bottom:0;
    border-radius: 50%;
  }
  nav.top { display: flex; gap: 22px; }
  nav.top a {
    font-family: var(--f-mono); font-size: .72rem; letter-spacing: .12em;
    text-transform: uppercase; text-decoration: none; color: var(--muted);
    padding: 6px 0; border-bottom: 2px solid transparent; transition: color .15s, border-color .15s;
  }
  nav.top a:hover { color: var(--ink); border-color: var(--stitch); }
  @media (max-width: 620px){ nav.top { display: none; } }

  .hero { padding: clamp(52px, 9vw, 104px) 0 clamp(40px,6vw,64px); }
  .eyebrow {
    font-family: var(--f-mono); font-size: .74rem; letter-spacing: .22em;
    text-transform: uppercase; color: var(--grass); margin: 0 0 18px;
    display: flex; align-items: center; gap: 12px;
  }
  .eyebrow::after { content:""; flex:1; height:1px; background: var(--line); }
  h1.name {
    font-family: var(--f-display);
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: -0.01em;
    line-height: .9;
    margin: 0;
    font-size: clamp(2.6rem, 10vw, 6.4rem);
    text-wrap: balance;
  }
  .tagline {
    margin: 18px 0 0;
    font-family: var(--f-display);
    font-weight: 700; font-style: italic;
    font-size: clamp(1.25rem, 3.2vw, 2rem);
    color: var(--stitch);
    letter-spacing: -.01em;
  }
  .lede { max-width: 46ch; margin: 22px 0 0; font-size: 1.075rem; color: var(--muted); }

  section { padding: clamp(46px, 7vw, 82px) 0; }
  .sec-kicker {
    font-family: var(--f-mono); font-size: .72rem; letter-spacing: .2em;
    text-transform: uppercase; color: var(--muted);
  }
  h2.sec-title {
    font-family: var(--f-display); font-weight: 800; text-transform: uppercase;
    letter-spacing: -.01em; line-height: 1; margin: 6px 0 0;
    font-size: clamp(1.9rem, 5vw, 3.1rem); text-wrap: balance;
  }
  .sec-sub { color: var(--muted); margin: 14px 0 0; max-width: 54ch; }

  .card {
    margin-top: 30px; background: var(--card);
    border: 1px solid var(--line); border-radius: 6px;
    box-shadow: var(--shadow); overflow: hidden;
  }
  .card-top {
    display: flex; justify-content: space-between; align-items: center;
    padding: 14px 20px; border-bottom: 2px dashed var(--stitch);
    font-family: var(--f-mono); font-size: .72rem; letter-spacing: .16em;
    text-transform: uppercase; color: var(--muted);
  }
  .card-body { padding: 26px 20px 30px; }

  textarea {
    width: 100%; min-height: 110px; resize: vertical;
    background: var(--paper); color: var(--ink);
    border: 1px solid var(--line); border-radius: 4px;
    font-family: var(--f-body); font-size: 1rem; line-height: 1.5;
    padding: 12px 14px;
  }
  .btn {
    font-family: var(--f-mono); font-size: .78rem; letter-spacing: .08em;
    text-transform: uppercase; text-decoration: none;
    padding: 12px 18px; border-radius: 2px; border: 1.5px solid var(--ink);
    display: inline-flex; align-items: center; gap: .55em;
    background: transparent; color: var(--ink); cursor: pointer;
    transition: transform .12s ease, background .15s, color .15s;
  }
  .btn:hover { transform: translateY(-2px); }
  .btn.primary { background: var(--stitch); border-color: var(--stitch); color: #fff; }
  .btn.primary:hover { background: color-mix(in srgb, var(--stitch) 88%, #000); }
  .btn[disabled] { opacity: .55; cursor: wait; transform: none; }

  pre.answer {
    margin: 18px 0 0; padding: 16px;
    background: var(--paper); border: 1px solid var(--line); border-radius: 4px;
    font-family: var(--f-mono); font-size: .88rem;
    white-space: pre-wrap; word-break: break-word;
    overflow-x: auto;
  }
  .answer[hidden] { display: none; }
  .status {
    font-family: var(--f-mono); font-size: .72rem; letter-spacing: .12em;
    text-transform: uppercase; color: var(--muted); margin-top: 12px;
  }

  footer {
    border-top: 2px dashed var(--stitch);
    padding: 48px 0 60px; margin-top: 20px;
  }
  .foot-grid { display: flex; justify-content: space-between; align-items: flex-end; gap: 28px; flex-wrap: wrap; }
  .foot-name { font-family: var(--f-display); font-weight: 800; text-transform: uppercase;
    font-size: clamp(1.6rem, 5vw, 2.4rem); letter-spacing: -.01em; line-height: 1; }
  .foot-links { display: flex; flex-direction: column; gap: 8px; }
  .foot-links a { font-family: var(--f-mono); font-size: .82rem; letter-spacing: .04em;
    color: var(--muted); text-decoration: none; }
  .foot-links a:hover { color: var(--stitch); }
  .copyright { margin-top: 26px; font-family: var(--f-mono); font-size: .72rem;
    letter-spacing: .1em; text-transform: uppercase; color: var(--muted); }
</style>
</head>
<body>

<header class="bar">
  <div class="wrap">
    <a class="wordmark" href="https://www.matt-jones.org/"><span class="ball" aria-hidden="true"></span> Matt Jones</a>
    <nav class="top" aria-label="Primary">
      <a href="https://www.matt-jones.org/">Home</a>
      <a href="https://www.matt-jones.org/about">About</a>
      <a href="https://www.matt-jones.org/portfolio">Portfolio</a>
      <a href="https://www.matt-jones.org/calendar">Book a time</a>
    </nav>
  </div>
</header>

<main>
  <section class="hero">
    <div class="wrap">
      <p class="eyebrow">From the dugout &nbsp;·&nbsp; Software</p>
      <h1 class="name">AICompared</h1>
      <p class="tagline">One prompt, every arm in the bullpen.</p>
      <p class="lede">Compare responses across AI providers. Throw a prompt and see what comes back.</p>
    </div>
  </section>

  <div class="wrap"><div class="stitch" aria-hidden="true"></div></div>

  <section id="ask">
    <div class="wrap">
      <span class="sec-kicker">At bat</span>
      <h2 class="sec-title">Ask a Question</h2>
      <p class="sec-sub">Your prompt goes to the configured provider and the answer shows up below.</p>

      <div class="card">
        <div class="card-top">
          <span>Prompt · AICompared</span>
          <span class="mono" id="providers">&nbsp;</span>
        </div>
        <div class="card-body">
          <form id="ask-form">
            <textarea id="prompt" name="prompt" placeholder="What do you want to know?" required></textarea>
            <div style="margin-top:14px; display:flex; gap:12px; align-items:center;">
              <button class="btn primary" type="submit" id="submit">Send it <span aria-hidden="true">&rarr;</span></button>
              <span class="status" id="status"></span>
            </div>
          </form>
          <pre class="answer" id="answer" hidden></pre>
        </div>
      </div>
    </div>
  </section>
</main>

<footer>
  <div class="wrap">
    <div class="stitch" aria-hidden="true" style="margin-bottom:34px;"></div>
    <div class="foot-grid">
      <div>
        <div class="foot-name">Let's talk ball.</div>
        <p class="sec-sub" style="margin-top:12px;">Interested in what I'm building here? Drop a line — I answer.</p>
      </div>
      <div class="foot-links">
        <a href="mailto:mscottjones24@gmail.com">mscottjones24@gmail.com</a>
        <a href="https://linkedin.com/in/mattjoneshtx">linkedin.com/in/mattjoneshtx</a>
        <a href="https://www.matt-jones.org/calendar">Book a time &rarr;</a>
      </div>
    </div>
    <div class="copyright">&copy; Matt Jones, 2026 — A website about nothing.</div>
  </div>
</footer>

<script>
  (function () {
    fetch("/providers").then(function (r) { return r.json(); }).then(function (d) {
      var el = document.getElementById("providers");
      var list = (d && d.configured) || [];
      el.textContent = list.length ? list.join(" · ") : "no providers configured";
    }).catch(function () {});

    var form = document.getElementById("ask-form");
    var button = document.getElementById("submit");
    var status = document.getElementById("status");
    var answer = document.getElementById("answer");

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var prompt = document.getElementById("prompt").value.trim();
      if (!prompt) return;
      button.disabled = true;
      status.textContent = "Pitching\\u2026";
      answer.hidden = true;
      fetch("/ask", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ prompt: prompt })
      }).then(function (r) { return r.json(); }).then(function (d) {
        answer.textContent = d.error ? "Error: " + d.error : (d.text || JSON.stringify(d, null, 2));
        answer.hidden = false;
        status.textContent = "";
      }).catch(function (err) {
        answer.textContent = "Request failed: " + err;
        answer.hidden = false;
        status.textContent = "";
      }).finally(function () {
        button.disabled = false;
      });
    });
  })();
</script>

</body>
</html>
`;
