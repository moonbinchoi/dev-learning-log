// Self-check: node practice-guard.test.js
const assert = require('assert');
const path = require('path');
const { run } = require('./practice-guard');

const root = path.resolve(__dirname, '..', '..');
const file = path.join(root, 'projects', 'docker-lab', 'compose.yaml');
const denied = (tool, tool_input, extra = {}) => !!run({ tool_name: tool, tool_input, cwd: root, ...extra });
const fwd = root.replace(/\\/g, '/'); // E:/Study/Inflearn
const gitBash = fwd.replace(/^([a-z]):/i, (_, d) => '/' + d.toLowerCase()); // /e/Study/Inflearn

assert(denied('Read', { file_path: file }));
assert(denied('Read', { file_path: 'projects/shop/src/App.java' })); // relative to cwd
assert(denied('Grep', { pattern: 'x', path: 'projects/shop' }));
assert(denied('Bash', { command: 'cat projects/docker-lab/compose.yaml' }));
assert(denied('Bash', { command: 'cat ./projects/shop/App.java' }));
assert(denied('Bash', { command: `cat ${fwd}/projects/shop/App.java` }));
assert(denied('Bash', { command: `cat ${gitBash}/projects/shop/App.java` }));
assert(denied('Bash', { command: 'grep -r foo projects' }));
assert(denied('PowerShell', { command: 'Get-Content projects\\docker-lab\\compose.yaml' }));
assert(denied('PowerShell', { command: `Get-Content "${root}\\projects\\shop\\App.java"` }));
assert(denied('Bash', { command: 'grep foo projects/docker-lab/Dockerfile ; docker ps ; git -C projects/docker-lab status' })); // compound: judged per piece

assert(!denied('Read', { file_path: file }, { agent_id: 'a1' })); // subagent
assert(!denied('Read', { file_path: path.join(root, 'docs', 'learning', 'operating-rules.md') }));
assert(!denied('Read', { file_path: path.join(root, 'projects-old', 'x.md') })); // prefix lookalike
assert(!denied('Grep', { pattern: 'x' })); // no path: whole repo search
assert(!denied('Bash', { command: 'git -C projects/shop diff' }));
assert(!denied('Bash', { command: 'docker compose -f projects/docker-lab/compose.yaml ps' }));
assert(!denied('Bash', { command: 'git -C projects/docker-lab status' }));
assert(!denied('Bash', { command: 'docker ps; git -C projects/x status' }));
assert(!denied('Glob', { pattern: 'projects/**' })); // listing paths only
assert(!denied('Bash', { command: 'cat ~/.claude/projects/e--Study-Inflearn/memory/MEMORY.md' })); // outside the repo
assert(!denied('Bash', { command: 'cat C:/Users/x/.claude/projects/y.md' }));
assert(!denied('Bash', { command: 'cat docs/learning/operating-rules.md' }));

console.log('practice-guard: ok');
