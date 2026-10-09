export type Post = {
  slug: string
  title: string
  date: string
  publishedAt: string
  tag: string
  excerpt: string
  readTime: string
  image: string
  content: string[]
  sources?: { title: string; url: string }[]
  score?: { overall: number; accuracy: number }
  linkedinUrl?: string
}

const files = import.meta.glob('../content/posts/*.json', { eager: true, import: 'default' })

export const posts: Post[] = (Object.values(files) as Post[]).sort((a, b) =>
  b.publishedAt.localeCompare(a.publishedAt),
)