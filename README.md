# Best of the City Awards — website (GHL embed blocks)

Source code for the bestofthecityawards.com rebuild in GoHighLevel. Every section of
every page is a self-contained **Custom HTML** block you paste into a GHL page.
Designed by My Launch Partner.

## What's here

```
assets/            Logos with transparent backgrounds
  wordmark-dark.png    horizontal logo, for light backgrounds (header)
  wordmark-light.png   horizontal logo, for dark backgrounds (footer)
  stacked-dark.png     stacked logo, for light backgrounds
  stacked-light.png    stacked logo, for dark backgrounds (heroes)
  icon.png             emblem only (favicon / social avatar)
src/               Editable source (images use the {{ASSET_BASE}} token)
  global/head.html     fonts + all styles — goes in the site's Head Tracking Code ONCE
  global/header.html   header block — top of every page
  global/footer.html   footer block — bottom of every page
  pages/<page>/NN-*.html  page sections, in order
dist/              PASTE THESE into GHL (same files, real image URLs filled in)
preview/           Full-page previews — open in a browser to see each page
build.py           Rebuilds dist/ and preview/ after you edit src/
config.json        asset_base = where the logo files are hosted
```

## Setting it up in GHL

1. **Global styles (once):** Sites > Websites > this site > Settings > *Head Tracking Code* →
   paste all of `dist/global/head.html`. Every block depends on it.
2. **Each page:** add one full-width section per block, set section padding to 0 and
   width to full, add a **Custom HTML / Code** element, paste the block.
3. **Block order per page:**

| Page | Slug | Blocks (in order) |
|---|---|---|
| Home | `/` | header, home/01 … home/07, footer |
| Free Sedona Spotlight | `/free-sedona-business-interviews` | header, free-sedona-spotlight/01 … 05, footer |
| Nominate *(new)* | `/nominate` | header, nominate/01, footer |
| Cities | `/all-businesses-by-state` | header, cities/01, footer |
| Contact | `/contact` | header, contact/01, footer |
| Featured Businesses | `/featured-businesses` | header, home/04, home/07, footer |

Existing slugs are kept so current links and search rankings carry over.

**Faster option:** `dist/full-page/<page>.html` holds a whole page (styles, header, every
section and footer) for ONE Code element in a single full-width, 0-padding section. The
Home page in GHL is built this way.

4. **Forms:** Nominate and Contact have a yellow form slot. Paste the GHL form's embed
   code there (Sites > Forms > form > Integrate), or delete the slot and drop a native
   GHL form element right after the block.

## Before going live — fill these in

Anything still needing a real value is wrapped in `<span class="bca-todo">` and shows
**bright yellow** on the page. Search `src/` for `bca-todo`:

- `[VOTING OPEN DATE]` — home season bar
- `[APPLICATION DEADLINE, incl. year]` — Free Spotlight hero and availability section (2 places)
- `[PASTE GHL … FORM EMBED CODE HERE]` — Nominate and Contact

Confirm these statements are true before publishing (they're new copy):

- "Buying a media package never affects nominations, votes or results" (home Promise + FAQ)
- Winners receive a physical award by mail (the old FAQ said both "mailed" and "upon request")
- Nominations and voting are always free (new FAQ question)
- Location: the site now says **Sedona, AZ** everywhere (the old Contact page said Flagstaff)

## What changed from the Webflow site

- Removed the placeholder testimonials (Willow Boutique, Apex Fitness, Brightside Café); the only quote is Jamie Inglett's real one
- Removed expired "December 2025" / "February 1st" dates; dates are now fill-in placeholders, and the footer year updates itself
- Fixed the package value: $499 + $2,499 = **$2,998** (was $2,999)
- Every "See How It Works" button scrolls to a real section; added a real `/nominate` page
- Cities page shows only live cities plus "Suggest a city," instead of 50 empty states; Arizona link is `/state/arizona`
- Accredited Interchange moved from "businesses we've featured" to a disclosed program-partner line in the footer
- Added an "award you can't buy" section explaining how winners are chosen
- Removed duplicated paragraphs and template agency copy; all images have alt text; logo files renamed

## Editing

Edit files in `src/`, then run `python3 build.py` and re-paste the changed block from `dist/`.
All CSS classes start with `bca-` so they can't collide with GHL's styles. Colors and fonts
are variables at the top of `src/global/head.html`.
