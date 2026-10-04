import { Link } from 'react-router-dom'

export default function Nav() {
  return (
    <nav
      className="fixed top-0 left-0 right-0 z-50 grid grid-cols-3 items-center px-8 md:px-14 py-3"
      style={{ background: 'rgba(253,251,248,0.35)', backdropFilter: 'blur(16px) saturate(180%) brightness(1.08)', WebkitBackdropFilter: 'blur(16px) saturate(180%) brightness(1.08)' }}
    >
      <div aria-hidden="true" className="absolute inset-0 pointer-events-none opacity-[0.035]" style={{ backgroundImage: "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='g'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='300' height='300' filter='url(%23g)'/%3E%3C/svg%3E\")", backgroundRepeat: 'repeat', backgroundSize: '200px 200px' }} />
      <Link
        to="/"
        className="text-[13px] tracking-[0.18em] uppercase text-[#0d0d0d] hover:text-[#a50000] transition-colors duration-200 flex items-center gap-1.5 group w-fit"
      >
        Journal
        <svg aria-hidden="true" width="9" height="9" viewBox="0 0 9 9" fill="none" className="opacity-0 group-hover:opacity-100 transition-opacity duration-200">
          <path d="M1 8L8 1M8 1H3.5M8 1V5.5" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      </Link>
      <span className="text-[15px] text-[#0d0d0d] text-center" style={{ letterSpacing: '-0.02em', fontWeight: 450 }}>
        pranavsankar.
      </span>
      <div className="flex justify-end">
        <a
          href="https://pranavsankar.me"
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
  )
}
