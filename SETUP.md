# Upload the complete profile

1. Extract the ZIP.
2. Open the public `usamafaheem-dev/usamafaheem-dev` repository.
3. Upload the CONTENTS of this folder to the repository root. Keep `assets`, `scripts` and `.github` intact. Do not upload this whole folder as a nested directory.
4. The repository root should have `README.md`, `dark.svg`, `light.svg`, `assets/`, `scripts/` and `.github/workflows/profile.yml`.
5. Commit the upload. Check the profile page to see the README.
6. Under Actions, enable workflows if GitHub asks, open **Refresh profile visuals**, and click **Run workflow**. The workflow will also refresh the local data cards daily when enabled. If Actions are disabled, the shipped dated cards still display.

The profile photo in `assets/profile-photo.jpg` is below 1 MB. Upload it separately in GitHub Settings → Public profile → Edit profile picture.

## What the numbers mean

- Indexed commits: public commits returned by GitHub commit search for the current year. They are not an all-time total or a count of private commits.
- Contributions: the public GitHub contribution calendar fetched through the open-source github-contributions-api mirror. If unavailable, the chart explicitly switches to public indexed commit activity.
- Language bars: the primary language of non-fork public repositories. They are repository counts, not percentages of code or skill levels.
- Recent commits: the five latest indexed authored commits, with repository, SHA, date and actual message.
- Data snapshot and sources: `assets/github-data.json`.

SVGs and icons are local assets. No third-party image-card service is needed to render the README. Data refresh needs GitHub API access; the calendar mirror is optional.

Original technology marks are from [Simple Icons](https://github.com/simple-icons/simple-icons), provided under CC0; trademark rights remain with their respective owners.
