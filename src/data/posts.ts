export type Post = {
  slug: string
  title: string
  date: string
  publishedAt: string
  tag: string
  excerpt: string
  readTime: string
  image: "/covers/prints-55264.webp",
  imageCredit: "Visit of the Empress to the Third National Industrial Promotional Exhibition at Ueno Park (Ueno dai sankai naikoku kangyō hakuran kai gyokō no zu), Yōshū (Hashimoto) Chikanobu, The Metropolitan Museum of Art, Open Access (CC0)",
  content: string[]
  sources?: { title: string; url: string }[]
  score?: { overall: number; accuracy: number }
  linkedinUrl?: string
}

const files = import.meta.glob('../content/posts/*.json', { eager: true, import: 'default' })

export const posts: Post[] = (Object.values(files) as Post[]).sort((a, b) =>
  b.publishedAt.localeCompare(a.publishedAt),
)