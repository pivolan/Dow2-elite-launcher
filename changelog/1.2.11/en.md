- GitHub Releases carry the same installers as the download folder, with the code signing policy in the notes.
- A release can also be published by hand for a patch version ("Run workflow" with "release" ticked), only from the
  commit its version tag points to.
- Windows builds are signed through SignPath only when they become a release.
