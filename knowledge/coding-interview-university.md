---
description: Map and caveats of jwasham/coding-interview-university, a multi-month CS-fundamentals study plan written for US big-tech interviews; use it as a topic checklist for data structures, algorithms and CS basics, not as a curriculum for Spring backend work.
source: https://github.com/jwasham/coding-interview-university
retrieved: 2026-10-19
why: Gives agents a vetted topic order and the author's own "what to skip" signals when planning or grading CS-fundamentals exercises, and states what the plan leaves out for a Spring backend learner.
refresh: yearly
---

# coding-interview-university (jwasham)

Summary in our own words; nothing is copied. The repo is CC-BY-SA-4.0, so a verbatim copy would carry ShareAlike. Facts checked against README.md and the GitHub API on 2026-10-19.

## What it is

- The author's "multi-month study plan for becoming a software engineer for a large company" (README, "What is it?"). Software engineering only; not frontend or full-stack.
- Status: ~363k stars. Last commit on `main` 2024-12-05 (recommended Python book changed to *Coding Interview Patterns*; sponsorship option removed). Not archived, but effectively dormant. Video links are likely partly dead (unchecked).

## Author's own caveats (use them when scoping)

- Knowing ~75% of a university CS program is "good enough for an interview", which is what the plan covers.
- Everything under "Additional Books" and below is "optional, NOT needed for an entry-level interview".
- Do not use the author's flashcards (too many, mostly trivia).
- DP: "you probably won't see any dynamic programming problems" in the interview, but recognizing it is worth it.
- Explicitly not covered: JavaScript, HTML/CSS, SQL.
- Language: the author used C (to feel pointers and memory) plus Python; one language you are comfortable with is enough for the coding rounds.
- System design questions are expected from ~4 years of experience; the plan puts it in the optional part.

## Topic order (main plan)

1. Complexity: Big-O, asymptotic analysis (watch and take notes, nothing to implement).
2. Data structures: arrays (build a vector), linked lists, stack, queue, hash table.
3. Binary search, bitwise operations.
4. Trees: traversals, BST, heap and priority queue.
5. Sorting: merge, quick, insertion, selection, heap.
6. Graphs: representations, BFS/DFS, shortest paths, spanning trees, topological sort.
7. More knowledge: recursion and backtracking, DP, design patterns, combinatorics and probability, NP-completeness, how a CPU runs programs, caches, processes and threads, testing, string search, tries, floating point, Unicode, endianness, networking.
8. Interview-specific close: final review, resume, process, mock interviews, behavioral stories, questions for the interviewer.

Optional part: more books, system design (the System Design Primer is the starting point), Unix tools, security basics, GC, messaging, probabilistic structures, balanced trees, SOLID, video series, university courses, classic papers.

## How to use it here

- Durable and useful as a checklist: items 1-7 above. Interview-specific and skippable: item 8, the whiteboard and flashcard advice, the "75%" framing.
- For a Spring backend learner it leaves out: SQL and database internals (indexes, transactions), the JVM, HTTP and API design beyond basic networking. Cover those from the Inflearn course material.
- If a course lesson and this plan order topics differently, keep the course's order and mention this plan only as a comparison.
- Do not cite its "75%" claim or star count as evidence of hiring outcomes; they are the author's statements and a popularity count.
