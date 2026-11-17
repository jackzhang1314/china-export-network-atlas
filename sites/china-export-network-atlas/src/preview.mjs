import { createReadStream, existsSync, statSync } from "node:fs";
import { createServer } from "node:http";
import { extname, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";

const root = fileURLToPath(new URL("../dist", import.meta.url));
const port = Number(process.env.PORT || 8787);
const mime = { ".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8", ".js": "text/javascript; charset=utf-8", ".svg": "image/svg+xml", ".webp": "image/webp", ".csv": "text/csv; charset=utf-8" };
if (!existsSync(resolve(root, "index.html"))) throw Error("请先运行 npm run build");

function serve(req, res) {
  const url = new URL(req.url, "http://localhost");
  let path;
  try { path = decodeURIComponent(url.pathname); }
  catch { res.writeHead(400).end(); return; }

  let file = resolve(root, "." + path);
  if (!file.startsWith(root + sep) && file !== root) {
    res.writeHead(404).end();
    return;
  }
  if (existsSync(file) && statSync(file).isDirectory()) {
    if (!path.endsWith("/")) {
      res.writeHead(307, { location: url.pathname + "/" + url.search }).end();
      return;
    }
    file = resolve(file, "index.html");
  }
  const found = existsSync(file) && statSync(file).isFile();
  if (!found) file = resolve(root, "404.html");
  res.writeHead(found ? 200 : 404, { "content-type": mime[extname(file)] || "application/octet-stream" });
  if (req.method === "HEAD") res.end();
  else createReadStream(file).pipe(res);
}

createServer(serve).listen(port, "127.0.0.1", () => console.log(`http://127.0.0.1:${port}/`));
