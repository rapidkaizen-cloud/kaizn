import { readFileSync } from 'node:fs'
import { defineConfig } from 'vitepress'

const REPO = 'https://github.com/rapidkaizen-cloud/kaizn'

// The sidebar is docs/README.md: each `## ` heading is a group, each table row that links
// a page of this folder is an item. One list serves the site, the GitHub folder view and
// `norms-help`, so a page is listed once.
function sidebar() {
  const index = readFileSync(new URL('../README.md', import.meta.url), 'utf8')
  const groups: { text: string; items: { text: string; link: string }[] }[] = []
  for (const line of index.split(/\r?\n/)) {
    const heading = line.match(/^## (.+)/)
    const row = line.match(/^\| \[([^\]]+)\]\((?!https?:|\.\.)([^)]+)\.md\)/)
    if (heading) groups.push({ text: heading[1], items: [] })
    else if (row && groups.length) groups.at(-1)!.items.push({ text: row[1], link: '/' + row[2] })
  }
  const filled = groups.filter((group) => group.items.length)
  if (!filled.length) throw new Error('docs/README.md lists no page: the sidebar would be empty')
  return filled
}

export default defineConfig({
  title: 'kaizn',
  description: 'kaizn settles an app one layer at a time and holds every later session to what was settled.',
  // Served as a project site: https://rapidkaizen-cloud.github.io/kaizn/
  base: '/kaizn/',
  cleanUrls: true,
  lastUpdated: true,
  // The queue is the toolkit's own work list, read on GitHub and by sessions here.
  srcExclude: ['queue.md'],
  rewrites: { 'README.md': 'index.md' },
  markdown: {
    config(md) {
      // VitePress compiles a page as a Vue template, where `{{` opens an expression. The
      // pages are plain Markdown, read on GitHub too, so no `{{` in them is one.
      for (const rule of ['text', 'code_inline'] as const) {
        const render = md.renderer.rules[rule]!
        md.renderer.rules[rule] = (...args) => render(...args).replaceAll('{{', '&#123;&#123;')
      }
    },
  },
  themeConfig: {
    nav: [
      { text: 'Get started', link: '/start/overview' },
      { text: 'Commands', link: '/reference/commands' },
      { text: 'Changelog', link: `${REPO}/blob/master/CHANGELOG.md` },
    ],
    sidebar: sidebar(),
    outline: { level: [2, 3] },
    search: { provider: 'local' },
    editLink: { pattern: `${REPO}/edit/master/docs/:path` },
    socialLinks: [{ icon: 'github', link: REPO }],
  },
})
