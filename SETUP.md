# Your complete GitHub profile

This package keeps your previous skills, project cards, GitHub statistics,
contributions, recent commits, experience and certifications. The old hero
has been replaced with your approved lime website design and moving badges.

## Upload to GitHub

1. Extract the ZIP. Do not upload the ZIP itself.
2. Open `usamafaheem-dev/usamafaheem-dev`.
3. Upload `README.md` and the complete `assets` folder to the repository root.
   Keep the folder structure. Do not put the assets loose in the root.
4. Also upload `scripts` and `.github` if you want the existing daily data refresh.
   The workflow file belongs at `.github/workflows/profile.yml`.
5. Commit the upload and open your public profile.

Expected structure:

```
README.md
assets/
  hero-animated.gif
  hero-static.png
  ...other profile visuals
scripts/
  update_profile.py
  build_snake.py
.github/
  workflows/
    profile.yml
```

## Preview before uploading

Open `PREVIEW.html`. It shows the complete profile with all local visuals.
The theme button is inside the profile card. Light mode is the default;
the button optionally switches the local preview to dark mode.
GitHub itself controls the theme of its profile page; a README cannot run
this custom preview button.
The standalone website is available at `website/index.html`.

The new website is connected at https://githubherowebisteusama.vercel.app/.
The README hero links to that site, not your older portfolio.
There are no extra navigation or Open website buttons outside the hero.
Portfolio/LinkedIn/email buttons are kept separately, as before.

GitHub renders the hero as an image and cannot run an embedded live website.
The navigation stays inside the hero artwork. In GitHub the whole hero is
one image link; individual painted labels cannot act as separate buttons.
PREVIEW.html embeds the corrected local website, whose menu changes pages
inside the hero. It does not embed the outdated deployed version.

## Update your Vercel website

The `website` folder contains the updated source with rounded corners and
no desktop three-line icon. The mobile menu remains available.
Push those files into your existing website project, preserving the assets
folder, and let Vercel redeploy. Your existing deployment URL stays the same.
The local preview already shows the corrected source. Your live Vercel URL
will show the updated version only after you push/redeploy the website files.

## GitHub data

Included cards preserve the previous dated public snapshot, not invented totals.
See `assets/github-data.json` for its date, sources and exact values.
In Actions, run **Refresh profile visuals** to update the data cards, or allow
its existing daily schedule to run. Uploading a workflow does not itself
confirm a successful refresh; check its completed run in GitHub Actions.
The included schedule is daily at 07:35 Pakistan time (02:35 UTC), not
instant or real-time. New public repositories, followers, stars, forks,
primary repository languages, indexed commits and activity appear after
the next successful refresh, subject to upstream indexing/cache delays.
The workflow must be on the default branch and Actions must be enabled.
You can use Run workflow for an on-demand refresh. GitHub scheduled jobs
can be delayed, so the displayed update date is the reliable timestamp.

Indexed commits are public search results for the labelled year, not an
all-time or private total. Language bars count repositories by primary language.

The contribution snake uses the same dated snapshot as the other cards.
The refresh workflow regenerates the snake after refreshing public data.
The hero's static image and non-animated calendar are used when a reader prefers reduced motion.
The supplied project screenshots are displayed in rounded, labelled image cards.
Original technology marks are credited in `assets/icon-sources.md`.
