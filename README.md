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
config.json        asset_base = where the logo files are hosted (jsDelivr, pinned to a commit so caches never go stale;
                   after changing a logo, commit it, then update the commit hash here and rebuild)
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
| Free Business Spotlight | `/free-business-spotlight` | header, free-business-spotlight/01 … 05, footer |
| Nominate *(new)* | `/nominate` | header, nominate/01, footer |
| Cities | `/all-businesses-by-state` | header, cities/01, footer |
| Contact | `/contact` | header, contact/01, footer |
| How It Works | `/how-it-works` | header, how-it-works/01, how-it-works/02, home/06, home/07, footer |
| Featured Businesses *(retired)* | `/featured-businesses` | forwards to `/spotlights` |
| 404 | site's 404 page | header, not-found/01, footer |

Existing slugs are kept so current links and search rankings carry over.

**Faster option:** `dist/full-page/<page>.html` holds a whole page (styles, header, every
section and footer) for ONE Code element in a single full-width, 0-padding section. The
Home page in GHL is built this way.

4. **Forms:** Nominate, Contact and Free Business Spotlight embed GHL forms ("BCA - Nominate a Business",
   "BCA - Contact Us" and "BCA - Free Spotlight Application" in Sites > Forms). Edit the fields in GHL;
   the pages update on their own. The spotlight form sits at `/free-business-spotlight#apply`.
   **Form styling:** GHL forms load in an iframe, so the site's styles can't reach them. Each form has
   `src/global/ghl-form.css` pasted into *Form builder > Styles & Options > Advanced > Custom CSS*.
   After editing that file, re-paste it into all three forms and save. The forms use a compact layout
   (two short fields per row); the page lets GHL's embed script size the iframe to fit.

## Before going live

Confirm these statements are true before publishing (they're new copy):

- "Buying a media package never affects nominations, votes or results" (home Promise + FAQ)
- Winners receive a physical award by mail (the old FAQ said both "mailed" and "upon request")
- Nominations and voting are always free (new FAQ question)
- Location: the site now says **Sedona, AZ** everywhere (the old Contact page said Flagstaff)

## What changed from the Webflow site

- Removed the placeholder testimonials (Willow Boutique, Apex Fitness, Brightside Café); the only quote is Jamie Inglett's real one
- Removed all Sedona-launch dates and deadlines; the spotlight offer is now a general Free Business Spotlight, and the footer year updates itself
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

## Business Spotlights (GHL blog, shown as "Spotlights")

Spotlights are GHL blog posts: Sites > Blogs > **Spotlights**. The list lives at `/spotlights`, each story at
`/post/<slug>`. The homepage "Meet our featured businesses" section pulls the 3 newest posts from `/spotlights`
automatically, so publishing a post updates the site with no code change.

**Add a new spotlight**
1. Copy `spotlights/content/_TEMPLATE.txt` to `spotlights/content/<slug>.txt` and fill it in (YouTube ID goes in `video:`).
2. Run `python3 build.py`. The post body appears in `dist/spotlights/posts/<slug>.html`.
3. In GHL: Spotlights > New post > clear the sample text > `<>` (custom code) > paste the body > Continue.
4. Settings: title, slug, canonical `bestofthecityawards.com/post/<slug>`, description, cover image + alt text,
   category = the city (e.g. "Sedona, AZ"), author = **Best of the City Awards**, keywords > Publish.
   With a video, the cover only shows on the Spotlights list (the video leads the story); without one, the cover shows on the story too.

**Templates:** the list and story page designs are in `src/spotlights/` (01/02 = list page top/bottom,
03/04 = story page top/bottom). They're pasted into the Spotlights blog builder (Edit blog site > Blog Home / Blog Post).
The header and footer live inside them, so re-paste all four when the header or footer changes.

## Known follow-ups

- **Destination Tattoo video:** add its YouTube ID to `spotlights/content/destination-tattoo-sedona.txt`, rebuild, and re-paste the post body.
- **Destination Tattoo cover** is their logo graphic; swap in a studio photo when available.
- **Form footer links** ("Privacy Policy | Terms of Service") in both GHL forms use GHL defaults; set real URLs.
