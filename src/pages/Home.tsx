import { useState } from 'react'
import { Link } from 'react-router-dom'
import branchImg from '../imports/ChatGPT_Image_Aug_10__2026__08_29_12_PM.png'
import avatarImg from '../imports/9.jpeg'
import Nav from '../components/Nav'
import { posts } from '../data/posts'

export default function Home() {
  const [hoverIdx, setHoverIdx] = useState<number | null>(null)

  return (
    <div className="min-h-screen overflow-x-hidden text-[#0d0d0d]" style={{ fontFamily: "'Inter', sans-serif", backgroundColor: '#fdfbf8' }}>
      <Nav />

      {/* ── HERO ── full viewport */}
      <section className="relative min-h-screen flex flex-col justify-center px-8 md:px-14">
        <img
          src={branchImg}
          aria-hidden="true"
          alt=""
          className="absolute pointer-events-none select-none"
          style={{
            top: '3%',
            right: '-6%',
            width: 'clamp(520px, 65vw, 820px)',
            height: 'auto',
            mixBlendMode: 'multiply',
            transformOrigin: '92% 30%',
            animation: 'branchSway 7s ease-in-out infinite',
          }}
        />

        <div className="max-w-3xl">
          <h1
            className="text-[clamp(2.8rem,7.5vw,6rem)] leading-[1.1] text-[#0d0d0d] mb-3"
            style={{ fontFamily: "'Outfit', sans-serif", fontWeight: 300, letterSpacing: '-0.03em' }}
          >
            we look for<br />
            <span style={{ fontWeight: 500 }}>what's changing.</span>
          </h1>
          <p
            className="text-[18px] leading-relaxed text-[#5a5a5a] max-w-md"
            style={{ fontFamily: "'Outfit', sans-serif", fontWeight: 300 }}
          >
            <a
              href="https://pranavsankar.me"
              target="_blank"
              rel="noopener noreferrer"
              className="text-[#0d0d0d] font-normal hover:font-medium underline-offset-2 hover:underline transition-all duration-200"
            >
              pranav sankar
            </a>
            's Journal on the Systems, Advances, and Ideas Redefining AI.
          </p>
        </div>

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

        <a
          href="https://pranavsankar.me"
          target="_blank"
          rel="noopener noreferrer"
          aria-label="Visit portfolio (opens in new tab)"
          className="absolute bottom-10 right-8 md:right-14 flex items-center gap-2.5 px-3 py-2 rounded-full group transition-all duration-200 hover:shadow-md"
          style={{ background: '#0d0d0d', border: '1px solid rgba(255,255,255,0.08)' }}
        >
          <img
            src={avatarImg}
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
        <div className="mb-14">
          <h2
            className="text-[clamp(2rem,4vw,3rem)] leading-[1.1] text-[#0d0d0d]"
            style={{ fontFamily: "'Outfit', sans-serif", fontWeight: 300, letterSpacing: '-0.02em' }}
          >
            <span style={{ fontWeight: 500 }}>Entries.</span>
          </h2>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-x-10 gap-y-16">
          {posts.map((post, i) => (
            <Link
              to={`/post/${post.id}`}
              key={post.id}
              className="group cursor-pointer block"
              onMouseEnter={() => setHoverIdx(i)}
              onMouseLeave={() => setHoverIdx(null)}
            >
              <article>
                <div className="relative w-full aspect-square overflow-hidden rounded-lg mb-4 bg-[#eeece6]">
                  <img
                    src={post.image}
                    alt=""
                    className="w-full h-full object-cover transition-all duration-500"
                    style={{
                      filter: hoverIdx === i ? 'grayscale(0%)' : 'grayscale(100%)',
                      transform: hoverIdx === i ? 'scale(1.03)' : 'scale(1)',
                    }}
                  />
                  <span
                    className="absolute top-3 left-3 px-2.5 py-1 rounded-full text-[10px] tracking-[0.14em] uppercase"
                    style={{ fontFamily: "'Space Mono', monospace", background: 'rgba(253,251,248,0.92)', color: '#0d0d0d' }}
                  >
                    {post.tag}
                  </span>
                </div>

                <span
                  className="text-[12px] text-[#9b9b9b] block mb-1.5"
                  style={{ fontFamily: "'Outfit', sans-serif", fontWeight: 300 }}
                >
                  {post.date}
                </span>

                <h3
                  className="text-[1.05rem] leading-snug mb-1.5 transition-colors duration-200"
                  style={{ fontFamily: "'Outfit', sans-serif", fontWeight: 500, color: hoverIdx === i ? '#a50000' : '#0d0d0d' }}
                >
                  {post.title}
                </h3>

                <p
                  className="text-[12.5px] leading-relaxed text-[#5a5a5a] mb-2"
                  style={{
                    fontFamily: "'Outfit', sans-serif",
                    fontWeight: 300,
                    display: '-webkit-box',
                    WebkitLineClamp: 2,
                    WebkitBoxOrient: 'vertical',
                    overflow: 'hidden',
                  }}
                >
                  {post.excerpt}
                </p>

                <span
                  className="text-[11px] tracking-[0.1em] uppercase text-[#9b9b9b]"
                  style={{ fontFamily: "'Space Mono', monospace" }}
                >
                  {post.readTime} read
                </span>
              </article>
            </Link>
          ))}
        </div>
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
