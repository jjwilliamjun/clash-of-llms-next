#!/usr/bin/env node
/**
 * Stop whatever is still listening on the dev ports.
 *
 * Why this exists: on Windows, killing a process does not kill its children, and
 * `npm run dev` nests several levels deep -- concurrently spawns a shell, which spawns
 * the command, and Flask's --debug reloader then forks a supervisor and a worker. Ctrl+C
 * does not always reach the bottom of that, and what survives keeps holding the port, so
 * the next `npm run dev` fails to bind with no obvious explanation.
 *
 * This kills by port rather than by process name, so it cannot take out an unrelated
 * python or node process that happens to be running.
 */
import { execFileSync } from "node:child_process";

const PORTS = [5000, 8080];
const isWindows = process.platform === "win32";

/** PIDs listening on `port`, or an empty array. */
function listenersOn(port) {
  try {
    if (isWindows) {
      const out = execFileSync("netstat", ["-ano", "-p", "TCP"], { encoding: "utf8" });
      return [
        ...new Set(
          out
            .split("\n")
            .filter((line) => /LISTENING/.test(line) && new RegExp(`:${port}\\s`).test(line))
            .map((line) => line.trim().split(/\s+/).pop())
            .filter((pid) => pid && pid !== "0"),
        ),
      ];
    }
    const out = execFileSync("lsof", ["-nP", `-iTCP:${port}`, "-sTCP:LISTEN", "-t"], {
      encoding: "utf8",
    });
    return [...new Set(out.split("\n").map((s) => s.trim()).filter(Boolean))];
  } catch {
    // Neither tool sets a zero exit code when nothing matches.
    return [];
  }
}

/** Kill `pid` and everything below it. */
function killTree(pid) {
  try {
    if (isWindows) {
      // /T takes the children with it -- the whole point of this script.
      execFileSync("taskkill", ["/PID", pid, "/T", "/F"], { stdio: "ignore" });
    } else {
      process.kill(-Number(pid), "SIGKILL");
    }
    return true;
  } catch {
    return false;
  }
}

for (const port of PORTS) {
  const pids = listenersOn(port);
  if (pids.length === 0) {
    console.log(`  :${port} already free`);
    continue;
  }

  for (const pid of pids) killTree(pid);

  // Report the port, not the individual kills. Killing one tree often takes a shared
  // ancestor with it, so a later taskkill fails only because its target is already
  // gone -- reporting that as "could not stop" reads like a failure when the port did
  // in fact come free.
  const left = listenersOn(port);
  if (left.length === 0) {
    console.log(`  :${port} freed (${pids.length} process tree${pids.length > 1 ? "s" : ""})`);
  } else {
    console.log(`  :${port} STILL HELD by PID ${left.join(", ")} — needs elevation?`);
  }
}

const remaining = PORTS.filter((port) => listenersOn(port).length > 0);
console.log(remaining.length === 0 ? "\nDev ports are free." : `\nStill held: ${remaining.join(", ")}`);
process.exit(remaining.length === 0 ? 0 : 1);
