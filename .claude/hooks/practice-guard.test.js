// Self-check: node practice-guard.test.js
const assert = require('assert');
const path = require('path');
const { run } = require('./practice-guard');

const root = path.resolve(__dirname, '..', '..');
const file = path.join(root, 'projects', 'docker-lab', 'compose.yaml');
const denied = (tool, tool_input, extra = {}) => !!run({ tool_name: tool, tool_input, cwd: root, ...extra });
const fwd = root.replace(/\\/g, '/'); // E:/Study/Inflearn
const app = 'projects/shop/src/main/java/com/study/shop/ShopApplication.java'; // exists: shell checks are existence-based
const gitBash = fwd.replace(/^([a-z]):/i, (_, d) => '/' + d.toLowerCase()); // /e/Study/Inflearn

assert(denied('Read', { file_path: file }));
assert(denied('Read', { file_path: 'projects/shop/src/App.java' })); // relative to cwd
assert(denied('Grep', { pattern: 'x', path: 'projects/shop' }));
assert(denied('Bash', { command: 'cat projects/docker-lab/compose.yaml' }));
assert(denied('Bash', { command: `cat ./${app}` }));
assert(denied('Bash', { command: `cat ${fwd}/${app}` }));
assert(denied('Bash', { command: `cat ${gitBash}/${app}` }));
assert(denied('Bash', { command: 'grep -r foo projects' }));
assert(denied('PowerShell', { command: 'Get-Content projects\\docker-lab\\compose.yaml' }));
assert(denied('PowerShell', { command: `Get-Content "${root}\\${app.replace(/\//g, '\\')}"` }));
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

// cwd inside a project: only tokens that resolve to an existing practice path count
const shopDir = path.join(root, 'projects', 'shop');
const inShop = (tool, command) => !!run({ tool_name: tool, tool_input: { command }, cwd: shopDir });
const outside = `${fwd}/docs/learning/operating-rules.md`;
assert(!inShop('Bash', `cat ${outside}`));
assert(!inShop('Bash', `cat ${gitBash}/docs/learning/operating-rules.md`));
assert(!inShop('Bash', `head -n 5 ${outside}`));
assert(!inShop('Bash', `sed -n 1,20p ${outside}`));
assert(!inShop('Bash', `cat ${outside} | grep -c TODO`));
assert(!inShop('Bash', `grep -n foo ${outside}`));
assert(!inShop('PowerShell', `Get-Content -Path ${outside}`));
assert(inShop('Bash', 'cat src/main/java/com/study/shop/ShopApplication.java'));
assert(inShop('Bash', 'grep -rn foo .'));
assert(inShop('Bash', 'cat src/main/java/com/study/shop/*.java')); // glob into an existing practice dir
assert(denied('Bash', { command: `cat ${app}` })); // cwd = repo root
assert(denied('Bash', { command: `${app} cat` })); // token position does not matter
assert(denied('Bash', { command: 'cd projects/shop && cat build.gradle' })); // cd moves the effective cwd
assert(denied('PowerShell', { command: 'Set-Location projects\\shop; Get-Content build.gradle' }));
assert(denied('Bash', { command: 'cat projects/shop/src/main/java/com/study/shop/*.java' }));
assert(!denied('Bash', { command: 'cat projects/shop/NoSuchFile.java' })); // nonexistent: reading nothing reveals nothing

// separators, cd that does not hide reads, globs, recursive reads
assert(denied('Bash', { command: 'cd projects/shop\ncat build.gradle' }));
assert(denied('Bash', { command: 'cd projects/shop\r\ncat build.gradle' }));
assert(denied('Bash', { command: 'cd docs\ncat E:/Study/Inflearn/projects/shop/build.gradle'.replace('E:/Study/Inflearn', fwd) })); // cd does not skip the read check
assert(denied('PowerShell', { command: `Set-Location docs\nGet-Content ${fwd}/projects/shop/build.gradle` }));
assert(denied('Bash', { command: 'cd /tmp & cat projects/shop/build.gradle' }));
assert(denied('Bash', { command: 'cd projects && cd shop && cat build.gradle' }));
assert(denied('Bash', { command: '<projects/shop/build.gradle cat' }));
assert(denied('Bash', { command: 'cat proj*/shop/build.gradle' }));
assert(denied('Bash', { command: 'cat */shop/build.gradle' }));
assert(denied('Bash', { command: 'grep -rn TODO .' }));
assert(denied('Bash', { command: 'grep -R TODO .' }));
assert(denied('Bash', { command: 'grep --recursive TODO .' }));
assert(!denied('Bash', { command: 'grep -rn TODO docs' }));
assert(!inShop('Bash', `head -n 5 ${outside}`));
assert(!inShop('Bash', `cat ${outside} | grep -c TODO`));

console.log('practice-guard: ok');
