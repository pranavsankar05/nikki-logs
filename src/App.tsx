import { useState } from 'react'

type Post = {
  id: number
  title: string
  date: string
  tag: string
  excerpt: string
  readTime: string
}

const posts: Post[] = [
  {
    id: 1,
    title: 'On building things that outlast you',
    date: '04 Aug 2026',
    tag: 'Craft',
    excerpt:
      "Every artefact we make is a small wager against forgetting. I've been thinking about what it means to build software with the same care a craftsman brings to physical objects.",
    readTime: '6 min',
  },
  {
    id: 2,
    title: 'The tyranny of the blank canvas',
    date: '19 Jul 2026',
    tag: 'Process',
    excerpt:
      "Constraints aren't limitations — they're the walls that give a room its shape. Starting from total freedom is the hardest condition to create well inside.",
    readTime: '4 min',
  },
  {
    id: 3,
    title: 'Attention as a design material',
    date: '02 Jul 2026',
    tag: 'Design',
    excerpt:
      "What if we measured interface quality not in clicks-to-task, but in how little of someone's cognitive presence we consumed to get them there?",
    readTime: '8 min',
  },
  {
    id: 4,
    title: 'Notes from a month of reading only long-form',
    date: '14 Jun 2026',
    tag: 'Reading',
    excerpt:
      'An experiment: no feeds, no aggregators, no summaries. Thirty days of books and long essays only, and what it quietly rearranged in how I think.',
    readTime: '5 min',
  },
  {
    id: 5,
    title: 'Why I keep a physical sketchbook in a digital job',
    date: '28 May 2026',
    tag: 'Tools',
    excerpt:
      "Paper doesn't autocorrect you. It doesn't suggest what you probably meant or flatten your handwriting into a neutral font. That friction is the point.",
    readTime: '3 min',
  },
  {
    id: 6,
    title: 'The case for finishing small projects',
    date: '10 May 2026',
    tag: 'Craft',
    excerpt:
      "There's a particular confidence that only comes from shipping. Not from planning or from learning — from the act of completing something, however modest.",
    readTime: '5 min',
  },
]

export default function App() {
  const [hoverIdx, setHoverIdx] = useState<number | null>(null)

  return (
    <div className="min-h-screen text-[#0d0d0d]" style={{ fontFamily: "'Inter', sans-serif", backgroundColor: '#fdfbf8' }}>

      {/* ── NAV ── 3-column spread */}
      <nav className="fixed top-0 left-0 right-0 z-50 grid grid-cols-3 items-center px-8 md:px-14 py-3"
        style={{ background: 'rgba(253,251,248,0.35)', backdropFilter: 'blur(16px) saturate(180%) brightness(1.08)', WebkitBackdropFilter: 'blur(16px) saturate(180%) brightness(1.08)' }}>
        <div aria-hidden="true" className="absolute inset-0 pointer-events-none opacity-[0.035]" style={{ backgroundImage: "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='g'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='300' height='300' filter='url(%23g)'/%3E%3C/svg%3E\")", backgroundRepeat: 'repeat', backgroundSize: '200px 200px' }} />
        <a
          href="#journal"
          className="text-[13px] tracking-[0.18em] uppercase text-[#0d0d0d] hover:text-[#a50000] transition-colors duration-200 flex items-center gap-1.5 group w-fit"
        >
          Journal
          <svg aria-hidden="true" width="9" height="9" viewBox="0 0 9 9" fill="none" className="opacity-0 group-hover:opacity-100 transition-opacity duration-200">
            <path d="M1 8L8 1M8 1H3.5M8 1V5.5" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        </a>
        <span className="text-[15px] text-[#0d0d0d] text-center" style={{ letterSpacing: '-0.02em', fontWeight: 450 }}>
          pranavsankar.
        </span>
        <div className="flex justify-end">
          <a
            href="https://example.com"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="Portfolio (opens in new tab)"
            className="text-[13px] tracking-[0.18em] uppercase text-[#6b6b6b] hover:text-[#a50000] transition-colors duration-200 flex items-center gap-1.5 group"
          >
            Portfolio
            <svg aria-hidden="true" width="9" height="9" viewBox="0 0 9 9" fill="none" className="opacity-40 group-hover:opacity-100 transition-opacity duration-200">
              <path d="M1 8L8 1M8 1H3.5M8 1V5.5" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          </a>
        </div>
      </nav>


      {/* ── HERO ── full viewport */}
      <section
        className="relative min-h-screen flex flex-col justify-center px-8 md:px-14"
        style={{}}
      >
        {/* cherry blossom branch — trunk from right, spreads left */}
        <img
          src="/src/imports/ChatGPT_Image_Aug_10__2026__08_29_12_PM.png"
          aria-hidden="true"
          alt=""
          className="absolute pointer-events-none select-none"
          style={{
            top: '3%',
            right: '-6%',
            width: 'clamp(420px, 55vw, 680px)',
            height: 'auto',
            mixBlendMode: 'multiply',
            transformOrigin: '92% 30%',
            animation: 'branchSway 7s ease-in-out infinite',
          }}
        />

        <div className="max-w-3xl">
          <h1
            className="text-[clamp(2.2rem,6vw,4.8rem)] leading-[1.1] text-[#0d0d0d] mb-3"
            style={{ fontFamily: "'Outfit', sans-serif", fontWeight: 300, letterSpacing: '-0.03em' }}
          >
            we look for<br />
            <span style={{ fontWeight: 500 }}>what's changing.</span>
          </h1>
          <p
            className="text-[15px] leading-relaxed text-[#5a5a5a] max-w-sm"
            style={{ fontFamily: "'Outfit', sans-serif", fontWeight: 300 }}
          >
            <a
              href="https://example.com"
              target="_blank"
              rel="noopener noreferrer"
              className="text-[#0d0d0d] font-normal hover:font-medium underline-offset-2 hover:underline transition-all duration-200"
            >
              pranav sankar
            </a>
            's Journal on the Systems, Advances, and Ideas Redefining AI.
          </p>
        </div>
        {/* scroll arrow — bottom center */}
        <a
          href="#journal"
          aria-label="Scroll to journal"
          className="absolute bottom-10 left-1/2 -translate-x-1/2 flex items-center justify-center rounded-full"
          style={{ width: 36, height: 36, background: '#0d0d0d', animation: 'scrollBounce 3s ease-in-out infinite' }}
        >
          <svg aria-hidden="true" width="12" height="20" viewBox="0 0 12 20" fill="none">
            <path d="M6 1v14M1 11l5 6 5-6" stroke="white" strokeWidth="1.2" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        </a>

        {/* portfolio button — bottom right */}
        <a
          href="https://example.com"
          target="_blank"
          rel="noopener noreferrer"
          aria-label="Visit portfolio (opens in new tab)"
          className="absolute bottom-10 right-8 md:right-14 flex items-center gap-2.5 px-3 py-2 rounded-full group transition-all duration-200 hover:shadow-md"
          style={{ background: '#0d0d0d', border: '1px solid rgba(255,255,255,0.08)' }}
        >
          <img
            src="/src/imports/9.jpeg"
            alt="Pranav Sankar"
            className="w-6 h-6 rounded-full object-cover object-top grayscale flex-shrink-0"
          />
          <span
            className="text-[11px] tracking-[0.18em] uppercase text-white group-hover:text-[#83F701] transition-colors duration-200 flex items-center gap-1.5"
            style={{ fontFamily: "'Space Mono', monospace" }}
          >
            Portfolio
            <svg aria-hidden="true" width="9" height="9" viewBox="0 0 9 9" fill="none" className="opacity-50 group-hover:opacity-100 transition-all duration-200 group-hover:translate-x-0.5 group-hover:-translate-y-0.5">
              <path d="M1 8L8 1M8 1H3.5M8 1V5.5" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          </span>
        </a>
      </section>

      {/* ── JOURNAL LIST ── */}
      <section id="journal" className="px-8 md:px-14 pt-20 pb-32 border-t border-[#e8e4de]">

        {/* section heading */}
        <div className="mb-14">
          <h2
            className="text-[clamp(2rem,4vw,3rem)] leading-[1.1] text-[#0d0d0d]"
            style={{ fontFamily: "'Outfit', sans-serif", fontWeight: 300, letterSpacing: '-0.02em' }}
          >
            <span style={{ fontWeight: 500 }}>Entries.</span>
          </h2>
        </div>

        {/* posts */}
        <ul>
          {posts.map((post, i) => (
            <li
              key={post.id}
              className="border-t border-[#e8e8e8] first:border-t-0"
              onMouseEnter={() => setHoverIdx(i)}
              onMouseLeave={() => setHoverIdx(null)}
            >
              <article className="group grid grid-cols-[140px_1fr] md:grid-cols-[180px_1fr] gap-6 md:gap-16 py-5">
                {/* left: date */}
                <span
                  className="text-[13px] text-[#6b6b6b] pt-1"
                  style={{ fontFamily: "'Outfit', sans-serif", fontWeight: 300 }}
                >
                  {post.date}
                </span>

                {/* right: title + excerpt + read time */}
                <div className="flex flex-col gap-2">
                  <h3
                    className="text-[0.95rem] md:text-[1rem] leading-snug flex items-baseline gap-3 transition-colors duration-200"
                    style={{ fontFamily: "'Outfit', sans-serif", fontWeight: 500, color: hoverIdx === i ? '#a83232' : '#0d0d0d' }}
                  >
                    {post.title}
                    <span
                      aria-hidden="true"
                      className="text-[#a50000] text-base transition-all duration-200"
                      style={{ opacity: hoverIdx === i ? 1 : 0, transform: hoverIdx === i ? 'translateX(0)' : 'translateX(-6px)', display: 'inline-block' }}
                    >
                      →
                    </span>
                  </h3>
                  <p
                    className="text-[12px] leading-relaxed max-w-xl transition-colors duration-200"
                    style={{ fontFamily: "'Outfit', sans-serif", fontWeight: 300, color: hoverIdx === i ? '#8a3a3a' : '#5a5a5a' }}
                  >
                    {post.excerpt}
                  </p>
                  <span
                    className="text-[12px] text-[#9b9b9b] mt-1"
                    style={{ fontFamily: "'Outfit', sans-serif", fontWeight: 300 }}
                  >
                    {post.readTime} read
                  </span>
                </div>
              </article>
            </li>
          ))}
        </ul>
      </section>

      {/* ── FOOTER ── */}
      <footer className="px-8 md:px-14 py-8 border-t border-[#e8e8e8] flex items-center justify-between">
        <span className="text-[12px] text-[#6b6b6b]" style={{ letterSpacing: '-0.01em' }}>
          pranav sankar
        </span>
        <span className="text-[11px] tracking-[0.15em] uppercase text-[#6b6b6b]" style={{ fontFamily: "'Space Mono', monospace" }}>
          {new Date().getFullYear()}
        </span>
      </footer>

    </div>
  )
}
