# LLM Container Escape & Isolation Testing

A security research project testing whether a compromised LLM deployment can break out of its Docker container to compromise the host system.

## Overview

This lab simulates a common real-world vulnerability pattern: an LLM application wrapper that executes model output as shell commands (a pattern seen in many "agentic" AI tool-calling implementations). The project tests whether this RCE can be escalated into a full container escape.

## Methodology

1. Built a deliberately vulnerable Flask-based LLM wrapper simulating unsafe tool execution
2. Containerized it with Docker to represent a typical production deployment
3. Achieved command injection RCE through the `/generate` endpoint
4. Systematically tested known container escape vectors:
   - Docker socket exposure
   - Host volume mount leakage
   - Privileged mode / device access
   - Linux capability abuse

## Key Findings

- **CRITICAL:** Command injection vulnerability grants full root RCE inside the container
- **CRITICAL:** Container runs as root (violates least privilege)
- **POSITIVE:** Docker socket not exposed - escape blocked
- **POSITIVE:** No host volume mounts - escape blocked
- **POSITIVE:** Not running in privileged mode - escape blocked

## Conclusion

Full container escape was not achieved due to proper Docker isolation. However, the application-level RCE combined with root execution represents a critical vulnerability that would result in full host compromise if combined with common misconfigurations (e.g., mounted Docker socket, privileged mode) seen in real-world CI/CD and dev environments.

## Files

- `dockerfiles/` - Vulnerable container build files
- `scripts/` - Testing and automation scripts
- `results/attack_log.md` - Full command/response evidence log
- `findings-report.md` - Detailed vulnerability findings and remediation

## Remediation

1. Never execute unsanitized model output as shell commands
2. Run containers as non-root user
3. Use read-only root filesystem
4. Drop unnecessary Linux capabilities (`--cap-drop=ALL`)
5. Never mount `docker.sock` into application containers
6. Use gVisor or similar sandboxing for untrusted LLM tool execution


## How to Reproduce This Project

### Prerequisites
- Kali Linux or any Linux distro
- Docker installed and running

### Setup Steps

1. Clone the repository
```bash
git clone https://github.com/YameenShaikh07/llm-container-escape.git
cd llm-container-escape
```

2. Build the vulnerable container
```bash
cd dockerfiles
docker build -t vulnerable-llm -f vulnerable_llm.Dockerfile .
cd ..
```

3. Run the container
```bash
docker run -d -p 5000:5000 --name llm-target vulnerable-llm
```

4. Verify it's running
```bash
docker ps
```

5. Send a test request
```bash
curl -X POST http://localhost:5000/generate -H "Content-Type: application/json" -d '{"prompt": "Hello AI"}'
```

6. Trigger the vulnerability
```bash
curl -X POST http://localhost:5000/generate -H "Content-Type: application/json" -d '{"prompt": "EXECUTE: whoami"}'
```

7. Clean up after testing
```bash
docker stop llm-target
docker rm llm-target
```

See `results/attack_log.md` for the full set of test cases and expected responses.







## Author

Yameen Shaikh  | AI Security Researcher | Penetration Tester | Security Analyst

## Disclaimer

For educational and authorized security research only. All testing performed against self-hosted, isolated lab infrastructure.
