import sublime, sublime_plugin, re

class WordCountCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		status = Helper.getAsString(self.view)

		if status:
			self.view.set_status("word_count", status)
		else:
			self.view.erase_status("word_count")

class WordCountPopupCommand(sublime_plugin.TextCommand):
	def run(self, edit, event):
		pos = self.view.layout_to_text((0, event["y"]))
		status = Helper.getAsHTML(self.view)

		if status:
			self.view.show_popup(status, flags=sublime.HIDE_ON_MOUSE_MOVE_AWAY, location=pos)

	def want_event(self):
		return True


class Helper():
	def getAsString(view):
		prefs = Helper.getSettings()
		words, chars, lines = Helper.countWords(view)

		return Helper.toString(Helper.toArray(words if prefs["words"] else None,
											  chars if prefs["chars"] else None,
											  lines if prefs["lines"] else None))

	def getAsHTML(view):
		prefs = Helper.getSettings()
		words, chars, lines = Helper.countWords(view)

		return Helper.toHTML(Helper.toArray(words if prefs["words"] else None,
											chars if prefs["chars"] else None,
											lines if prefs["lines"] else None))

	def getSettings():
		settings = {}
		set_file = sublime.load_settings("WordCount.sublime-settings")
		settings["words"] = set_file.get("show_word_count", True)
		settings["chars"] = set_file.get("show_char_count", True)
		settings["lines"] = set_file.get("show_line_count", True)
		return settings

	def countWords(view):
		region = sublime.Region(0, view.size())
		content = view.substr(region).strip()
		p = re.compile("\s+", re.MULTILINE)
		
		words = len(re.split(p, re.sub("[,.?!:;]", " ", content))) - 1
		chars = len(re.sub(p, "", content))
		lines = len(view.lines(region))

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
