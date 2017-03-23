# SimpleWordCount Sublime Plugin

This is a very simple ST3 plugin to count words, characters, and lines in the current file.

## Installation

Simply put the entire `WordCount` directory into your ST3 `Packages` directory.

## Usage

You can choose which counts to show by modifying the settings file.

To show a popup with your selected counts, select "Word Count" from the context menu (right click in any file to show the context menu). Alternatively, press `ctrl+shift+c` on Windows or `command+shift+c` on Mac to show your selected counts in the status bar.

## Settings

The following settings are available for customization:
* `show_word_count`: show count of words,
* `show_char_count`: show count of characters,
* `show_line_count`: show count of lines,
* `run_continuously`: update status bar whenever the file is modified, and,
* `time_delay`: time in seconds to wait between updates when running continuously.