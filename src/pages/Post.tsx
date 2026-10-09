import { Fragment } from 'react'
import { useParams, Link } from 'react-router-dom'
import avatarImg from '../imports/9.jpeg'
import cosmosImg from '../imports/cosmos_554930236.webp'
import Nav from '../components/Nav'
import { posts } from '../data/posts'

const AUTHOR_BIO =
  "I build things at the intersection of AI, full-stack development, and problem solving. Lately that means working with LLMs and APIs, agents, and orchestration. I like taking an idea from a rough sketch all the way to a working product."

const serif = "'Crimson Text', serif"
const body = "'Neco', 'Crimson Text', serif"

function Asterisk() {
  return (
    <svg width="7" height="7" viewBox="0 0 24 24" aria-hidden="true" className="inline-block mx-2 -translate-y-0.5">
      <g fill="#626262">
        <rect x="10.5" y="0" width="3" height="24" />
        <rect x="10.5" y="0" width="3" height="24" transform="rotate(60 12 12)" />
        <rect x="10.5" y="0" width="3" height="24" transform="rotate(120 12 12)" />
      </g>
    </svg>
  )
}

function Byline({ withBio }: { withBio: boolean }) {
  return (
    <div className={withBio ? 'flex items-start justify-between gap-10 flex-wrap' : ''}>
      <div className="flex items-center gap-3">
        <img
          src={avatarImg}
          alt="Pranav Sankar"
          className="w-[67px] h-[67px] rounded-full object-cover object-top grayscale flex-shrink-0"
        />
        <div>
          <div style={{ fontFamily: serif, fontSize: 16, letterSpacing: '-0.01em', color: '#000000' }}>
            pranav sankar s
          </div>
          <div style={{ fontFamily: serif, fontSize: 13, letterSpacing: '-0.01em', color: '#5C5151', marginTop: 2 }}>
            Full-Stack Developer &amp; AI Enthusiast
          </div>
          <a
            href="https://pranavsankar.me"
            target="_blank"
            rel="noopener noreferrer"
            style={{ fontFamily: serif, fontSize: 16, letterSpacing: '-0.01em', color: '#000000', textDecoration: 'underline', display: 'inline-block', marginTop: 2 }}
          >
            www.pranavsankar.me
          </a>
        </div>
      </div>

      {withBio && (
        <p
          className="max-w-[405px] text-right"
          style={{ fontFamily: serif, fontSize: 16, letterSpacing: '-0.07em', color: '#5C5151', lineHeight: 1.2, margin: 0 }}
        >
          {AUTHOR_BIO}
        </p>
      )}
    </div>
  )
}

export default function Post() {
  const { id } = useParams()
  const index = posts.findIndex((p) => p.slug === id)
  const post = posts[index]
  const next = posts[(index + 1) % posts.length]

  if (!post) {
    return (
      <div className="min-h-screen flex items-center justify-center" style={{ backgroundColor: '#FBF8F4' }}>
        <Link to="/" className="text-[13px] underline">
          Entry not found — back to Journal
        </Link>
      </div>
    )
  }

  const year = post.date.split(' ').pop()
  // Inline image breaks the body after the 3rd paragraph, matching the spec.
  const imageAfterIndex = 2

  return (
    <div className="min-h-screen" style={{ backgroundColor: '#FBF8F4', color: '#000000' }}>
      <Nav />

      <article className="px-8 md:px-[142px] pt-28 pb-20">
        <div className="max-w-[1152px] mx-auto">
          <Byline withBio />

          <div style={{ borderTop: '1px solid #000000', margin: '40px 0 44px' }} />

          <h1
            style={{
              fontFamily: serif,
              fontSize: 'clamp(2.6rem, 6vw, 6.25rem)',
              lineHeight: 0.9,
              letterSpacing: '-0.07em',
              color: '#000000',
              margin: '0 0 28px',
            }}
          >
            {post.title} .
          </h1>

          <div style={{ fontFamily: serif, fontSize: 16, letterSpacing: '0.05em', color: '#626262', marginBottom: 12 }}>
            {year}
            <Asterisk />
            {post.tag}
            <Asterisk />
            {post.readTime}
          </div>

          <p
            className="max-w-[516px]"
            style={{ fontFamily: serif, fontSize: 20, lineHeight: 1.27, letterSpacing: '-0.02em', color: '#6D5E5E', margin: '0 0 64px' }}
          >
            <span style={{ color: '#9b9b9b' }}>Excerpt: </span>
            {post.excerpt}
          </p>

          <div className="max-w-[895px]">
            {post.content.map((para, i) => (
              <Fragment key={i}>
                <p
                  style={{
                    fontFamily: body,
                    fontSize: 24,
                    lineHeight: 2.25,
                    letterSpacing: '-0.02em',
                    textAlign: 'justify',
                    color: '#000000',
                    margin: '0 0 8px',
                  }}
                >
                  {para}
                </p>
                {i === imageAfterIndex && (
                  <div
                    className="my-10 mx-auto"
                    style={{ width: 532, maxWidth: '100%', border: '38px solid #FFFFFF', boxShadow: '0 1px 2px rgba(0,0,0,0.08)' }}
                  >
                    <img
                      src={cosmosImg}
                      alt=""
                      style={{ width: '100%', aspectRatio: '532 / 376', objectFit: 'cover', display: 'block' }}
                    />
                  </div>
                )}
              </Fragment>
            ))}
          </div>

          <div className="mt-20 mb-16">
            <Byline withBio={false} />
          </div>

          <div style={{ borderTop: '1px solid #e8e4de' }} className="pt-7 flex items-center justify-between gap-6">
            <Link
              to="/"
              className="text-[12px] tracking-[0.14em] uppercase transition-colors duration-200"
              style={{ fontFamily: "'Space Mono', monospace", color: '#6b6b6b' }}
            >
              ← Journal
            </Link>
            <Link to={`/post/${next.slug}`} className="text-right group">
              <div
                className="text-[11px] tracking-[0.14em] uppercase mb-1"
                style={{ fontFamily: "'Space Mono', monospace", color: '#9b9b9b' }}
              >
                Next entry
              </div>
              <div
                className="text-[15px] group-hover:text-[#a50000] transition-colors duration-200"
                style={{ fontFamily: "'Outfit', sans-serif", fontWeight: 500, color: '#0d0d0d' }}
              >
                {next.title} <span style={{ color: '#a50000' }}>→</span>
              </div>
            </Link>
          </div>
        </div>
      </article>

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
