# wow_token
pulls wow token data from https://wowtokenprices.com and sends a push notification using [Pushover](https://pushover.net) if the current gold price is below your specified threshold.

## Requirements
Tested using Python v3.8

- Python 3
- [Pushover](https://pushover.net) (for push notifications)

## Setup
- Change the `push_price` variable to be your gold threshold. If WoW Tokens drop below this threshold you'll get a push notification.
- Add your Pushover `user_key` and `app_token`
- Setup a [LaunchAgent](https://www.launchd.info) (macOS), [Cron task](https://help.dreamhost.com/hc/en-us/articles/215767047-Creating-a-custom-Cron-Job) (Linux), or [Task](https://www.dummies.com/computers/pcs/how-to-open-windows-task-scheduler/) (Windows) to run the script

### macOS LaunchAgent
For macOS I've included a LaunchAgent that you can drop into your LaunchAgents folder.

Replace USER with your computer username
- Create /Users/USER/Library/LaunchAgents if it doesn't exist
- Copy com.bryanheinz.wow_token.plist to /Users/USER/Library/LaunchAgents
- Verify the Python 3 path is correct (might be `/usr/bin/python3`)
- Update the LaunchAgent with your path to wow_token_push.py
- Update the LaunchAgent with how often you want the script to be run (3600 == 1 hour in seconds)
- Reboot or run `/bin/launchctl bootstrap gui/$(/usr/bin/id -u) /Users/$(/usr/bin/whoami)/Library/LaunchAgents/com.bryanheinz.wow_token.plist` in Terminal
