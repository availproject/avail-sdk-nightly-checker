<p align="center">
<img align="center" src="avail-logo.png" width="250">
</p>

# Avail node docs nightly checker

This is the first iteration of a bot that runs a daily check of code snippets documented under [Avail's developer documentation](https://docs.availproject.org/) and checks for breakages.
We at Avail aim for a seamless developer experience with docs that work 100% of the time. This bot is an effort in that direction.


## How does it work? (This section is under progress)

- Avail currently offers three SDKs to developers to let them interact with the Avail node conviniently in a language of their choice: [Avail-js](https://github.com/availproject/avail-js), [Avail-rust](https://github.com/availproject/avail-rust), and [Avail-go](https://github.com/availproject/avail-go-sdk/).

- The bot runs every day at 00:00 hrs UTC via a Cron Job.

- The Cron job simply calls the [/main.py](https://github.com/availproject/avail-sdk-nightly-checker/blob/main/main.py).

- The script, in turn:
  1. Sets up local dev environments on a VM for the three SDKs under their own directories. The exact commands to set up these daily environments are fetched from the markdown of the docs. This ensures that the local env is set up exactly in line with what's in the docs.
  2. The bot then executes a series of scripts in a master-worker setup.
  3. Each individual script corresponds to a single snippet in the docs, for example [submit-data](https://docs.availproject.org/api-reference/avail-node-api/da-submit-data).
  4. It will fetch the latest code for its own snippet and execute it in each of the three SDK languages.
  5. The result of each specific run is logged in [run-results.json](https://github.com/availproject/avail-sdk-nightly-checker/blob/main/run-results.json)
  6. This process is repeated `n` times till all individual scripts have been executed.
  7. After this process is completed, the environments created for each of the SDKs are deleted, thus ensuring a fresh setup at every single run.
  8. The complete logs of each run are stored in [last-run-log.txt](https://github.com/availproject/avail-sdk-nightly-checker/blob/main/last-run-log.txt)
  9. Finally, the bot automatically pushes the latest versions of `run-results.json` & `last-run-log.txt` to this repo.
  10. This ensures that if we have any errors/breakage, we can diagnose the exact issue and push corrections to the docs conveniently.
