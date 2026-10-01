import re, html, sys
src = open("docs/privacy-policy.md", encoding="utf-8").read()
en_i = src.index("\n## English\n"); pt_i = src.index("\n## Português (Brasil)\n")
def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"`(.+?)`", r"<code>\1</code>", t)
    t = re.sub(r"\b([\w.+-]+@[\w-]+\.[\w.]+)\b", r'<a href="mailto:\1">\1</a>', t)
    t = re.sub(r"(<strong>)?(\[TODO[^\]]*\])(</strong>)?", r'<mark>\2</mark>', t)
    return t
def section(text):
    out = []
    for block in text.strip().split("\n\n"):
        block = block.strip()
        if block.startswith("---") or not block: continue
        if block.startswith("## "): out.append("<h2>%s</h2>" % inline(block[3:]))
        elif block.startswith("### "): out.append("<h3>%s</h3>" % inline(block[4:]))
        elif block.startswith("- "): out.append("<ul>%s</ul>" % "".join("<li>%s</li>" % inline(l[2:]) for l in block.split("\n")))
        elif block.startswith("**") and block.endswith("**") and "\n" not in block and block.count("**") == 2 and block.startswith(("**Village", "**Cerco")): out.append("<h1>%s</h1>" % inline(block[2:-2]))
        else: out.append("<p>%s</p>" % inline(block.replace("\n", " ")))
    return "\n".join(out)
en = section(src[en_i:pt_i].replace("## English", "", 1))
pt = section(src[pt_i:].replace("## Português (Brasil)", "", 1))
page = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Village Siege / Cerco da Vila: Privacy Policy / Política de Privacidade</title>
<style>
:root{--bg:#fbf8f2;--fg:#2b2118;--muted:#6b5a48;--accent:#4f7d3b;--line:#e2d9c8}
@media(prefers-color-scheme:dark){:root{--bg:#1f1812;--fg:#efe6d6;--muted:#b8a68e;--accent:#8fc06f;--line:#3a2f24}}
body{margin:0;background:var(--bg);color:var(--fg);font:17px/1.6 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
main{max-width:46rem;margin:0 auto;padding:1.5rem 1rem 4rem}
nav{display:flex;gap:1rem;padding:.75rem 0;border-bottom:1px solid var(--line);margin-bottom:1rem}
a{color:var(--accent)} h1{font-size:1.6rem;margin:.5rem 0} h2{margin-top:3rem;border-top:1px solid var(--line);padding-top:1rem}
h3{margin:1.6rem 0 .3rem;font-size:1.1rem} p,ul{margin:.5rem 0} mark{background:#ffe680;color:#000;padding:0 .2em}
</style></head><body><main>
<nav><a href="#en">English</a><a href="#pt">Português (Brasil)</a></nav>
<section id="en" lang="en"><h2>English</h2>
%s
</section>
<section id="pt" lang="pt-BR"><h2>Português (Brasil)</h2>
%s
</section>
</main></body></html>
""" % (en, pt)
open(sys.argv[1], "w", encoding="utf-8", newline="\n").write(page)
