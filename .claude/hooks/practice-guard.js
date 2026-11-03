// Practice guard for docs/learning/operating-rules.md: practice code under projects/ is graded by reviewer with grading.md, even one file.
// Denies the main session's reads of projects/; subagents pass. Hook event: PreToolUse.
const path = require('path');

const PRACTICE = path.resolve(__dirname, '..', '..', 'projects').toLowerCase();
const SHELL_READ = /\b(cat|type|head|tail|less|more|sed|awk|grep|rg|get-content|gc|select-string|sls)\b/i;
const SHELL_OK = /^\s*(git|docker)\b/i; // diff for the review talk, status reads: both main-session exceptions

const inPractice = (p, cwd) => {
  const abs = path.resolve(cwd || process.cwd(), String(p)).toLowerCase();
  return abs === PRACTICE || abs.startsWith(PRACTICE + path.sep);
};
// Git Bash writes E:\x as /e/x.
const fromGitBash = (t) => t.replace(/^\/([a-z])\//i, '$1:/');

function run(input) {
  if (input.agent_id) return null; // fired inside a subagent
  const t = input.tool_input || {};
  let hit = false;
  if (input.tool_name === 'Read') hit = inPractice(t.file_path, input.cwd);
  else if (input.tool_name === 'Grep') hit = !!t.path && inPractice(t.path, input.cwd);
  else if (input.tool_name === 'Bash' || input.tool_name === 'PowerShell') {
    const c = String(t.command || '');
    // ponytail: naive split, a separator inside quotes also splits; parse quotes if that causes false denies.
    hit = c.split(/;|&&|\|\|?/).some(
      (s) =>
        SHELL_READ.test(s) &&
        !SHELL_OK.test(s) &&
        s.split(/[\s"'=<>(),]+/).some((tok) => tok && inPractice(fromGitBash(tok), input.cwd))
    );
  }
  if (!hit) return null;
  return {
    hookSpecificOutput: {
      hookEventName: 'PreToolUse',
      permissionDecision: 'deny',
      permissionDecisionReason:
        'operating-rules.md: practice files under projects/ are graded by `reviewer` with docs/learning/grading.md, even a single file. Dispatch reviewer with grading.md, the file paths, and the course material; talk the review through with the user from its result and git diff. Commands starting with git or docker pass; run them as separate calls.',
    },
  };
}

module.exports = { run };

if (require.main === module) {
  let raw = '';
  process.stdin.on('data', (c) => (raw += c));
  process.stdin.on('end', () => {
    try {
      const out = run(JSON.parse(raw));
      if (out) process.stdout.write(JSON.stringify(out));
    } catch (e) {
      // fail open: a guard bug must not block the session
    }
  });
}
