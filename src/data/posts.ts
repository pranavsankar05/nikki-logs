export type Post = {
  id: number
  title: string
  date: string
  tag: string
  excerpt: string
  readTime: string
  image: string
  content: string[]
}

export const posts: Post[] = [
  {
    id: 1,
    title: 'On building things that outlast you',
    date: '04 Aug 2026',
    tag: 'Craft',
    excerpt:
      "Every artefact we make is a small wager against forgetting. I've been thinking about what it means to build software with the same care a craftsman brings to physical objects.",
    readTime: '6 min',
    image: 'https://picsum.photos/seed/craft1/600/750',
    content: [
      "Every artefact we make is a small wager against forgetting. I've been thinking about what it means to build software with the same care a craftsman brings to physical objects — a chair that's expected to hold weight for forty years, a joint cut so it tightens rather than loosens with use.",
      "Most of what I ship doesn't need to last. A script runs once and is discarded; a prototype proves a point and is thrown away. That's fine — not everything deserves permanence. But the things that do deserve it get a different kind of attention: fewer dependencies, clearer names, decisions explained in comments not for the next sprint but for whoever reads this in three years and has no memory of why it's shaped this way.",
      "Craftsmanship isn't about perfection. It's about leaving a thing in a state where someone else — or future you — can pick it up without resentment. That's the whole bar. Most days, it's enough.",
    ],
  },
  {
    id: 2,
    title: 'The tyranny of the blank canvas',
    date: '19 Jul 2026',
    tag: 'Process',
    excerpt:
      "Constraints aren't limitations — they're the walls that give a room its shape. Starting from total freedom is the hardest condition to create well inside.",
    readTime: '4 min',
    image: 'https://picsum.photos/seed/canvas2/600/750',
    content: [
      "Constraints aren't limitations — they're the walls that give a room its shape. Starting from total freedom is the hardest condition to create well inside, and I think most people who say they're \"stuck\" are actually just unconstrained.",
      "Give me a blank page and infinite time and I'll produce nothing. Give me a deadline, a word limit, and someone else's half-finished draft to react to, and I'll produce something by Thursday. The scaffolding isn't a compromise — it's the thing that makes starting possible at all.",
      "I've started manufacturing fake constraints when real ones aren't around. Fifteen-minute timers. Arbitrary rules — no more than three colors, no more than one dependency. They're artificial, and they work anyway, because the brain doesn't seem to care whether a wall is load-bearing. It just needs one to push against.",
    ],
  },
  {
    id: 3,
    title: 'Attention as a design material',
    date: '02 Jul 2026',
    tag: 'Design',
    excerpt:
      "What if we measured interface quality not in clicks-to-task, but in how little of someone's cognitive presence we consumed to get them there?",
    readTime: '8 min',
    image: 'https://picsum.photos/seed/design3/600/750',
    content: [
      "What if we measured interface quality not in clicks-to-task, but in how little of someone's cognitive presence we consumed to get them there? Most design metrics optimize for speed. Almost none optimize for what's left of a person's attention once the task is done.",
      "A notification that pulls you out of deep work for a 'congratulations, you did the thing' moment has cost more than its three seconds on screen — it costs the four minutes it takes to find your way back into the thought you were having. That cost never shows up in any dashboard, because nobody's measuring it.",
      "Treating attention as a material — something with a finite supply, that can be spent well or wasted — changes what 'good design' means. Not frictionless. Not even fast. Quiet. The best interface is the one you forget you were using, because it never asked for more of you than the task actually required.",
    ],
  },
  {
    id: 4,
    title: 'Notes from a month of reading only long-form',
    date: '14 Jun 2026',
    tag: 'Reading',
    excerpt:
      'An experiment: no feeds, no aggregators, no summaries. Thirty days of books and long essays only, and what it quietly rearranged in how I think.',
    readTime: '5 min',
    image: 'https://picsum.photos/seed/reading4/600/750',
    content: [
      "An experiment: no feeds, no aggregators, no summaries. Thirty days of books and long essays only, and what it quietly rearranged in how I think.",
      "The first week was the hardest, and not for the reason I expected. It wasn't willpower — it was that my attention span had genuinely shortened, and a twelve-page essay felt like running a mile after months of only walking to the mailbox. By week two, that resistance was gone, replaced by something I'd forgotten: the specific pleasure of an argument that takes its time to arrive somewhere.",
      "What surprised me most wasn't how much I retained — it was how much better I got at noticing when a short piece was hiding a thin argument behind confident formatting. Feeds train you to mistake pace for substance. A month away from them was enough to partially untrain it.",
    ],
  },
  {
    id: 5,
    title: 'Why I keep a physical sketchbook in a digital job',
    date: '28 May 2026',
    tag: 'Tools',
    excerpt:
      "Paper doesn't autocorrect you. It doesn't suggest what you probably meant or flatten your handwriting into a neutral font. That friction is the point.",
    readTime: '3 min',
    image: 'https://picsum.photos/seed/sketch5/600/750',
    content: [
      "Paper doesn't autocorrect you. It doesn't suggest what you probably meant or flatten your handwriting into a neutral font. That friction is the point.",
      "Every digital tool I use is, in some small way, trying to help me finish the thought faster. Usually that's good. But some thoughts aren't ready to be finished — they need to sit half-formed on a page for a while, messy and wrong in places, before they're worth typing anywhere permanent.",
      "The sketchbook is where the bad ideas live before I know they're bad. Keeping that space analog means nothing is watching, nothing is suggesting, and nothing is quietly nudging the idea toward whatever shape the software expects it to take.",
    ],
  },
  {
    id: 6,
    title: 'The case for finishing small projects',
    date: '10 May 2026',
    tag: 'Craft',
    excerpt:
      "There's a particular confidence that only comes from shipping. Not from planning or from learning — from the act of completing something, however modest.",
    readTime: '5 min',
    image: 'https://picsum.photos/seed/craft6/600/750',
    content: [
      "There's a particular confidence that only comes from shipping. Not from planning or from learning — from the act of completing something, however modest.",
      "I have more unfinished ambitious projects than I can count, and for a long time I thought that was a pipeline problem — too many ideas, not enough hours. It wasn't. It was that none of them were small enough to actually finish, so each one quietly taught me that finishing wasn't really expected of me.",
      "A small project, actually completed, teaches a different lesson: that the gap between idea and working thing is crossable, on a timeline you can hold in your head. That lesson doesn't scale down from the big projects. It has to be learned small first.",
    ],
  },
]
