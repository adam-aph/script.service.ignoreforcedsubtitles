# service.IgnoreForcedSubtitles
This is a simple and small Kodi service that replaces forced subtitles with complete subtitles in the same language.

## Usage
- Set your preferred subtitle language in the Kodi Player's subtitle options.
- No further action is required, as the plugin operates on the following logic:
  - Find the preferred language for the currently assigned subtitle stream.
  - Loop through all available subtitles of the same preferred language.
  - Assign the first subtitle that is not marked as 'forced.'

### Notes
This is Python 3 plugin, works only with Kodi version > 19.

Hopefully, future versions of Kodi will include an 'ignore forced subtitles' option by default, rendering this plugin unnecessary.