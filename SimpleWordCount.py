import sublime, sublime_plugin, re, time

settings = {}
lastTime = time.time()

class WordCountCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		status = Helper.getAsString(self.view)

		if status:
			self.view.set_status("word_count", status)
		else:
			self.view.erase_status("word_count")

class WordCountPopupCommand(sublime_plugin.TextCommand):
	def run(self, edit, event):
		pos = self.view.window_to_text((event["x"], event["y"]))
		status = Helper.getAsHTML(self.view)

		if status:
			self.view.show_popup(status, flags=sublime.HIDE_ON_MOUSE_MOVE_AWAY, location=pos)

	def want_event(self):
		return True

class WordCountListener(sublime_plugin.EventListener):
	def on_modified_async(self, view):
		global lastTime
		
		prefs = Helper.getSettings()
		if prefs["watch"] and time.time() - lastTime > prefs["delay"]:
			lastTime = time.time()
			status = Helper.getAsString(view)

			if status:
				view.set_status("word_count", status)
			else:
				view.erase_status("word_count")

class Helper():
	def getAsString(view):
		prefs = Helper.getSettings()
		words, chars, lines = Helper.countWords(view, prefs)

		return Helper.toString(Helper.toArray(words if prefs["words"] else None,
											  chars if prefs["chars"] else None,
											  lines if prefs["lines"] else None))

	def getAsHTML(view):
		prefs = Helper.getSettings()
		words, chars, lines = Helper.countWords(view, prefs)

		return Helper.toHTML(Helper.toArray(words if prefs["words"] else None,
											chars if prefs["chars"] else None,
											lines if prefs["lines"] else None))

	def getSettings():
		global settings

		if settings:
			return settings
		settings = {}
		set_file = sublime.load_settings("SimpleWordCount.sublime-settings")
		settings["words"] = set_file.get("show_word_count", True)
		settings["chars"] = set_file.get("show_char_count", True)
		settings["lines"] = set_file.get("show_line_count", True)
		settings["watch"] = set_file.get("run_continuously", False)
		settings["delay"] = set_file.get("time_delay", 1)
		return settings

	def countWords(view, prefs):
		region = sublime.Region(0, view.size())
		content = view.substr(region).strip()
		p = re.compile("\s+", re.MULTILINE)
		
		words = len(re.split(p, re.sub("[,.?!:;]", " ", content))) - 1 if prefs["words"] else None
		chars = len(re.sub(p, "", content)) if prefs["chars"] else None
		lines = len(view.lines(region)) if prefs["lines"] else None

		return (words, chars, lines)

	def toArray(words, chars, lines):
		elements = []
		if words:
			elements.append("Words: " + str(words))
		if chars:
			elements.append("Chars: " + str(chars))
		if lines:
			elements.append("Lines: " + str(lines))

		return elements

	def toString(elements):
		return " | ".join(elements) if len(elements) > 0 else None

	def toHTML(elements):
		return "<br>".join(elements) if len(elements) > 0 else None
