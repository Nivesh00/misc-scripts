# ghcr-clean-images

Script deletes all images that are untagged in the ghcr (i.e. images that have the SHA commit as the tag and start with `sha`)

## Running script

- Set variables in the `.env` file, token should have read/write access to packages and/or repo
  ```env
  REPOSITORY=
  GITHUB_TOKEN=
  ```

- Run script using following command
  ```bash
  cd misc-scripts/ghcr-clean-images
  py delete-untagged-images.py
  ```