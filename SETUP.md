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
  hero-static.jpg
  ...other profile visuals
scripts/
  update_profile.py
.github/
  workflows/
    profile.yml
```

## Preview before uploading

Open `PREVIEW.html`. It shows the complete profile with all local visuals.
The live website is separate: open `website/index.html`.

The profile hero links to your existing portfolio at https://usamafaheem.com/.
The new website has not been published. If you publish it, replace the first
link in README.md with its real hosted URL. Do not use a localhost link on GitHub.

GitHub renders the hero as an image, so its drawn navigation is decorative.
The buttons under the hero are real links. The navigation inside the separate
website is interactive.

## GitHub data

Included cards preserve the previous dated public snapshot, not invented totals.
See `assets/github-data.json` for its date, sources and exact values.
In Actions, run **Refresh profile visuals** to update the data cards, or allow
its existing daily schedule to run. Uploading a workflow does not itself
confirm a successful refresh; check its completed run in GitHub Actions.

Indexed commits are public search results for the labelled year, not an
all-time or private total. Language bars count repositories by primary language.

The hero's static image is used when a reader prefers reduced motion.
Original technology marks are credited in `assets/icon-sources.md`.
